import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { text, lang } = await req.json();

    if (!text) {
      return NextResponse.json({ error: "Text payload is required." }, { status: 400 });
    }

    const hfToken = process.env.HUGGINGFACE_API_KEY;
    if (!hfToken) {
      return NextResponse.json(
        { error: "HUGGINGFACE_API_KEY is not configured on the server." },
        { status: 500 }
      );
    }

    const model = lang === "hin" ? "ResembleAI/chatterbox" : "espnet/kan-bayashi_ljspeech_vits";

    // Set a 6-second timeout so the UI instantly falls back if network DNS hangs
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const response = await fetch(
      `https://router.huggingface.co/hf-inference/models/${model}`,
      {
        headers: {
          Authorization: `Bearer ${hfToken.trim()}`,
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({
          inputs: text,
          options: { wait_for_model: true },
        }),
        signal: controller.signal,
      }
    );

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: errorText || "Hugging Face inference failed." },
        { status: response.status }
      );
    }

    const audioArrayBuffer = await response.arrayBuffer();

    return new NextResponse(audioArrayBuffer, {
      status: 200,
      headers: {
        "Content-Type": "audio/wav",
        "Content-Length": audioArrayBuffer.byteLength.toString(),
      },
    });
  } catch (error: any) {
    console.warn("⚠️ Hugging Face unreachable / network error, falling back to Web Speech:", error.message);
    return NextResponse.json(
      { error: "NETWORK_FALLBACK", details: error.message },
      { status: 503 }
    );
  }
}