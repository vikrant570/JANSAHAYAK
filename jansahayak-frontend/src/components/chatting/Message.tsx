"use client";

import { useState, useRef, useEffect } from "react";
import {
  LuEllipsisVertical,
  LuVolume2,
  LuSquare,
  LuThumbsUp,
  LuThumbsDown,
  LuRecycle,
  LuLoader,
} from "react-icons/lu";
import { TextNormalizer } from "@/lib/normalizer";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

interface Msg {
  _id: string;
  chatID: string;
  role: string;
  content: string;
  createdAt: string;
}

interface MessageProps {
  message: Msg;
}

const Message = ({ message }: MessageProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const playBrowserSpeechFallback = (text: string, isHindi: boolean) => {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    setIsLoading(false);
    setIsPlaying(false);
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  const voices = window.speechSynthesis.getVoices();

  if (isHindi) {
    const hindiVoice =
      voices.find((v) => v.lang === "hi-IN" || v.lang.startsWith("hi")) ||
      voices.find((v) => v.name.toLowerCase().includes("hindi") || v.name.includes("Lekha") || v.name.includes("Hemant")) ||
      voices.find((v) => v.lang === "en-IN");
    if (hindiVoice) utterance.voice = hindiVoice;
    utterance.lang = "hi-IN";
  } else {
    // English voice
    const englishVoice =
      voices.find((v) => v.lang === "en-IN") ||
      voices.find((v) => v.lang.startsWith("en"));
    if (englishVoice) utterance.voice = englishVoice;
    utterance.lang = "en-US";
  }

  utterance.rate = 0.95;  utterance.pitch = 1.0;

  utterance.onstart = () => {
    setIsLoading(false);
    setIsPlaying(true);
  };
  utterance.onend = () => setIsPlaying(false);
  utterance.onerror = () => {
    setIsLoading(false);
    setIsPlaying(false);
  };

  window.speechSynthesis.speak(utterance);
};

  const handleToggleAudio = async () => {
    if (isPlaying) {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      setIsPlaying(false);
      return;
    }

    const sanitizedText = TextNormalizer.normalize(message.content);
    if (!sanitizedText) return;

    const isHindi = TextNormalizer.isHindiText(sanitizedText);
    const lang = isHindi ? "hin" : "eng";

    try {
      setIsLoading(true);

      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: sanitizedText, lang }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        console.warn("HF API error, switching to browser Web Speech fallback:", errData);
        playBrowserSpeechFallback(sanitizedText, isHindi);
        return;
      }

      const audioBlob = await res.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      const audio = new Audio(audioUrl);
      audioRef.current = audio;

      audio.onplay = () => {
        setIsLoading(false);
        setIsPlaying(true);
      };

      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

      audio.onerror = () => {
        console.warn("Audio playback failed, falling back to Web Speech.");
        playBrowserSpeechFallback(sanitizedText, isHindi);
      };

      await audio.play();
    } catch (err) {
      console.warn("Fetch error, invoking browser fallback:", err);
      playBrowserSpeechFallback(sanitizedText, isHindi);
    }
  };

  return (
    <div
      className={`flex ${message.role === "assistant" ? "self-start" : "self-end mr-1 md:mr-0"
        } max-w-[90%] h-fit flex-col w-fit gap-2`}
    >
      {message.role === "assistant" && (
        <span className="flex gap-2 items-center self-end text-texts-dark/60">
          <button
            type="button"
            onClick={handleToggleAudio}
            disabled={isLoading}
            title={isPlaying ? "Stop audio" : "Play message audio"}
            aria-label={isPlaying ? "Stop audio" : "Play message audio"}
            className={`p-1 rounded-full transition-colors cursor-pointer ${isPlaying
              ? "text-sky-500 bg-sky-500/10 animate-pulse"
              : "hover:text-texts-dark focus:bg-ui-tertiary"
              }`}
          >
            {isLoading ? (
              <LuLoader size={15} className="animate-spin text-sky-500" />
            ) : isPlaying ? (
              <LuSquare size={14} />
            ) : (
              <LuVolume2 size={16} />
            )}
          </button>
          <LuEllipsisVertical size={16} />
        </span>
      )}
      {
        message.role === "assistant" ?
          <div className="bg-ui-tertiary/50 rounded-2xl min-w-[90%] p-4 text-texts-dark">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
              components={{
                h2: ({ node, ...props }) => <h2 className="text-lg md:text-xl font-bold mt-2 mb-1" {...props} />,
                h3: ({ node, ...props }) => <h3 className="text-md md:text-lg font-semibold mt-2 mb-1" {...props} />,
                a: ({ node, ...props }) => <a className="text-indigo-500 underline" target="_blank" rel="noopener noreferrer" {...props} />,
                strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                hr: ({ node, ...props }) => <hr className="my-2 border-ui-tertiary" {...props} />,
                p: ({ node, ...props }) => <p className="mb-1 text-sm md:text-md" {...props} />,
              }}
            >
              {(() => {
                const cleanContent = typeof message.content === 'string'
                  ? message.content.replace(/\\n/g, '\n')
                  : message.content;
                return cleanContent;
              })()}
            </ReactMarkdown>
          </div>
          :
          <div className="bg-buttons/15 shadow-md shadow-black/10 text-texts-dark px-4 py-2 rounded-2xl w-fit h-fit" >
            {message.content}
          </div>
      }
      {message.role === "assistant" && (
        <span className="flex gap-2 items-center self-start ml-1 text-texts-dark/60">
          <LuThumbsUp size={15} className="cursor-pointer hover:text-texts-dark" />
          <LuThumbsDown size={15} className="cursor-pointer hover:text-texts-dark" />
          <LuRecycle size={15} className="cursor-pointer hover:text-texts-dark" />
        </span>
      )}
    </div>
  );
};

export default Message;