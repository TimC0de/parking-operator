import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Input,
  Text,
  Container,
  Flex,
  Avatar,
  IconButton,
  Spinner, Button,
} from '@chakra-ui/react';
import {LuMic, LuSearch} from 'react-icons/lu';
import { api } from '../utils/api';
import axios from 'axios';
//
// import "react-use-audio-recorder/dist/index.css";
import VoiceMessageComponent from "./VoiceMessageComponent.tsx";

enum RequestType {
  TEXT_REQUEST = "TEXT_REQUEST",
  VOICE_REQUEST = "VOICE_REQUEST"
}

interface Message {
  id: string;
  type: RequestType;
  value: string | Blob;
  isUser: boolean;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isChatFinished, setIsChatFinished] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const bgColor = ['gray.50', 'gray.800'];
  const messageBg = ['white', 'gray.600'];
  const userMessageBg = ['blue.500', 'blue.600'];
  const borderColor = ['gray.200', 'gray.600'];

  // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        stream.getTracks().forEach(track => track.stop());

        console.log('Recorded...');
        sendMessage(RequestType.VOICE_REQUEST, blob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const createNewChat = () => {
    setMessages([]);
    setInputValue('');
    setError(null);
    setIsChatFinished(false);
  }

  const closeConversation = async () => {
    try {
      await api.post('/api/resolve/close');
    } catch (err) {
      console.error('Error closing conversation:', err);
    }
  }

  const sendMessage = async (
      request_type: RequestType,
      request_value: string | Blob,
  ) => {
    if (isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: request_type,
      value: typeof request_value === 'string' ? request_value.trim() : request_value,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('request_type', request_type);

      if (request_type == RequestType.TEXT_REQUEST) {
        formData.append('request_value', request_value);
      } else {
        formData.append('request_value', request_value, "voice.mp3");
      }

      const result = await api.post(
        '/api/resolve/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: RequestType.TEXT_REQUEST,
        value: result.data.response! || "I'm sorry, I couldn't generate a response.",
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);

      if (result.data.is_finished) {
        setIsChatFinished(true);
        await closeConversation();
      }
    } catch (err) {
      console.error('Error calling endpoint:', err);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: RequestType.TEXT_REQUEST,
        value: "Sorry, I encountered an error while processing your message.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(RequestType.TEXT_REQUEST, inputValue);
    }
  };

  return (
    <Container maxW="4xl" h="90vh" p={0}>
      <Flex direction="column" h="full">
        {/* Header */}
        <Box
          p={4}
          borderBottom="1px"
          borderColor={borderColor}
          bg={messageBg}
          shadow="sm"
        >
          <HStack justify="space-between">
            <Text fontSize="lg" fontWeight="bold">
              Parking Operator Chat
            </Text>
            <HStack>
              <Box
                w={3}
                h={3}
                borderRadius="full"
                bg={'green.400'}
              />
              <Text fontSize="sm" color="gray.500">
                Connected
              </Text>
            </HStack>
          </HStack>
        </Box>

        {/* Error Alert */}
        {error && (
            <div>{error}</div>
        )}

        {/* Messages Area */}
        <Box
          flex="1"
          overflowY="auto"
          bg={bgColor}
          p={4}
        >
          <VStack spacing={4} align="stretch">
            {messages.length === 0 && !isLoading && (
              <Box textAlign="center" py={8}>
                <Text color="gray.500" fontSize="lg">
                  Welcome to Parking Operator! 🚗
                </Text>
                <Text color="gray.400" fontSize="sm" mt={2}>
                  Ask me anything about parking regulations, rates, or finding parking spots.
                </Text>
              </Box>
            )}

            {messages.map((message) => (
              <HStack
                key={message.id}
                align="start"
                justify={message.isUser ? 'flex-end' : 'flex-start'}
                spacing={3}
              >
                {/*{!message.isUser && (*/}
                {/*  <Avatar size="sm" name="Operator" bg="blue.500" />*/}
                {/*)}*/}

                <Box
                  maxW="70%"
                  bg={message.isUser ? userMessageBg : messageBg}
                  color={message.isUser ? 'white' : 'inherit'}
                  p={3}
                  borderRadius="lg"
                  borderBottomLeftRadius={message.isUser ? 'lg' : 'sm'}
                  borderBottomRightRadius={message.isUser ? 'sm' : 'lg'}
                  shadow="sm"
                >
                  {message.type === RequestType.TEXT_REQUEST && (<Text>{message.value}</Text>)}
                  {message.type === RequestType.VOICE_REQUEST && (<VoiceMessageComponent audioBlob={message.value} />)}

                  <Text
                    fontSize="xs"
                    opacity={0.7}
                    mt={1}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </Text>
                </Box>

                {/*{message.isUser && (*/}
                {/*  <Avatar size="sm" name="You" bg="gray.500" />*/}
                {/*)}*/}
              </HStack>
            ))}

            {isLoading && (
              <HStack align="start" spacing={3}>
                {/* <Avatar size="sm" name="Operator" bg="blue.500" /> */}
                <Box
                  bg="white"
                  p={3}
                  borderRadius="lg"
                  borderBottomLeftRadius="sm"
                  shadow="sm"
                >
                  <HStack>
                    <Spinner size="sm" />
                    <Text>Thinking...</Text>
                  </HStack>
                </Box>
              </HStack>
            )}

            {isChatFinished && (
                <Box textAlign="center" py={4}>
                    <Text color="gray.500" fontSize="md" mb={2}>
                      The chat has ended. Start a new conversation?
                    </Text>
                    <Button
                      aria-label="New Chat"
                      onClick={createNewChat}
                      color="white"
                    >
                      New Chat
                    </Button>
                </Box>
            )}

            <div ref={messagesEndRef} />
          </VStack>
        </Box>

        {/* Input Area */}
        <Box
            p={4}
            borderTop="1px"
            borderColor={borderColor}
            bg={messageBg}
        >
          <HStack spacing={2}>
            <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your parking command..."
                disabled={isLoading}
                bg={bgColor}
                border="1px"
                borderColor={borderColor}
                _focus={{
                  borderColor: 'blue.500',
                  boxShadow: '0 0 0 1px blue.500',
                }}
            />
            <IconButton
                aria-label="Send message"
                onClick={() => sendMessage(RequestType.TEXT_REQUEST, inputValue)}
                isDisabled={!inputValue.trim() || isLoading}
                isLoading={isLoading}
                size="md"
            >
              <LuSearch color="white"/>
            </IconButton>

            {!isRecording && (
              <IconButton
                  aria-label="Start Recording"
                  size="md"
                  onClick={startRecording}
              >
                <LuMic color="white" />
              </IconButton>
            )}

            {isRecording && (
              <IconButton
                  aria-label="Start Recording"
                  size="md"
                  onClick={stopRecording}
              >
                <LuMic color="red" />
              </IconButton>
            )}
          </HStack>
        </Box>
      </Flex>
    </Container>
  );
};

export default ChatInterface;