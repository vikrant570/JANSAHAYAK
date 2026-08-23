"use client";
import { useState, useRef, useEffect, SetStateAction } from "react";
import { LuMic, LuMicOff, LuArrowUp, LuPlus, LuAudioWaveform } from "react-icons/lu";
import { Msg } from "@/components/chatting/ChatInterface";
import api from "@/lib/axiosInstance";
import { handleAxiosError } from "@/utils/handleError";
import { useToastMsgContext } from "@/contexts/ToastMsgContext";
import { useRouter } from "next/navigation";
import { Chat } from "./SideBar";

interface Props {
  setNewMessage: React.Dispatch<SetStateAction<Msg | null>>;
  setCurrentChat: React.Dispatch<SetStateAction<{ _id: string; title: string; } | null>>;
  currentChat: { _id: string; title: string; } | null;
  setChats: React.Dispatch<SetStateAction<Chat[] | null>>
}

const PromptBar = ({ setNewMessage, setCurrentChat, currentChat, setChats }: Props) => {
  const [prompt, setPrompt] = useState<string>("");
  const [isListening, setIsListening] = useState<boolean>(false);
  const recognitionRef = useRef<any>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const { showToastMsg } = useToastMsgContext();

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        // en-IN allows seamless recognition of Indian English and Hinglish terms
        // Change to "hi-IN" for pure Hindi transcription
        recognition.lang = "en-IN";

        recognition.onresult = (event: any) => {
          let currentTranscript = "";
          for (let i = 0; i < event.results.length; i++) {
            currentTranscript += event.results[i][0].transcript;
          }
          setPrompt(currentTranscript);
        };

        recognition.onerror = (event: any) => {
          console.error("Speech recognition error:", event.error);
          setIsListening(false);
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error("Failed to start speech recognition:", err);
      }
    }
  };

  const chatNotOpened = async () => {
    const newChat = await api.put("/chats", { title: prompt.split(" ", 3).join(" ") });
    const createdChat = {
      _id: newChat.data.chat._id || "",
      title: newChat.data.chat.title || "",
      user: newChat.data.chat.user || "",
      createdAt: newChat.data.chat.createdAt || "",
      updatedAt: newChat.data.chat.updatedAt || ""
    }

    setCurrentChat(createdChat);
    setChats(prev => prev ? [...prev, createdChat] : [createdChat]);
    return createdChat;
  }

  const handleSend = async () => {
    if (!prompt.trim() || !setNewMessage) return;
    const messageForChat = currentChat && setNewMessage !== undefined ? currentChat : await chatNotOpened();

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }

    const newMessage = {
      _id: Date.now().toString(),
      chatID: messageForChat?._id || " ",
      role: "user",
      content: prompt.trim(),
      createdAt: new Date().toISOString()
    };
    setNewMessage(newMessage);

    try {
      const response = await api.post("/agent/chat", { prompt: prompt.trim(), chatID: messageForChat?._id == "" || !messageForChat ? undefined : messageForChat?._id });
      if (!response.data.status) throw new Error();


      const agentResponseMessage = {
        _id: Date.now().toString(),
        chatID: messageForChat?._id || "",
        role: "assistant",
        content: response.data.answer,
        createdAt: new Date().toISOString()
      }
      setNewMessage(agentResponseMessage);
    }
    catch (error) {
      showToastMsg({ text: handleAxiosError(error), type: "error" })
    }
    finally {
      setPrompt("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(e.target.value);
    const el = textareaRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = `${Math.min(el.scrollHeight, 128)}px`; // 128px = max-h-32 equivalent
    }
  };

  return (
    <span className="min-w-70 md:min-w-180 relative min-h-fit flex items-end justify-between border-ui-tertiary/10 border-2 px-5 py-2 rounded-3xl bg-white z-10 shadow-sm">
      <div className="flex flex-row items-center mb-2 justify-between flex-1">
        <span className="relative w-fit h-fit text-texts-secondary mr-1.5 cursor-pointer hover:bg-ui-tertiary/60 hover:text-texts-dark rounded-full px-1 py-1 transition-colors duration-100">
          <LuPlus size={16} />
        </span>
        <textarea
          ref={textareaRef}
          className="flex-1 text-black resize-none bg-transparent outline-none text-xs md:text-sm wrap-anywhere scrollbar-thumb-ui-tertiary scrollbar-thin max-h-32"
          placeholder={isListening ? "Listening... Speak now" : "Ask anything on your mind . . ."}
          value={prompt}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          rows={1}
        />
      </div>

      <div className="flex flex-row items-center gap-0 md:gap-2">
        <button
          type="button"
          onClick={toggleListening}
          title={isListening ? "Stop recording" : "Start voice input"}
          className={`p-3 rounded-full transition-all duration-150 shrink-0 cursor-pointer ${isListening
            ? "bg-buttons text-texts-primary animate-pulse"
            : "text-texts-secondary hover:bg-ui-tertiary/60 hover:text-black"
            }`}
        >
          {isListening ? <LuAudioWaveform size={16} /> : <LuMic size={16} />}
        </button>

        <button
          type="button"
          onClick={handleSend}
          disabled={prompt.trim() === ""}
          className="bg-buttons disabled:opacity-40 disabled:cursor-not-allowed p-3 rounded-full hover:bg-buttons/70 transition-colors duration-150 shrink-0 text-white"
        >
          <LuArrowUp size={16} />
        </button>
      </div>
    </span>
  );
};

export default PromptBar;