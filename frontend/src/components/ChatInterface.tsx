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
  Spinner,
} from '@chakra-ui/react';
import {LuMic, LuSearch} from 'react-icons/lu';
import { api } from '../utils/api';

import "react-use-audio-recorder/dist/index.css";
import { useAudioRecorder } from "react-use-audio-recorder";


interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

enum RequestType {
  TEXT_REQUEST = "TEXT_REQUEST",
  VOICE_REQUEST = "VOICE_REQUEST"
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const {
    recordingStatus,
    startRecording,
    stopRecording,
  } = useAudioRecorder();

  const bgColor = ['gray.50', 'gray.800'];
  const messageBg = ['white', 'gray.600'];
  const userMessageBg = ['blue.500', 'blue.600'];
  const borderColor = ['gray.200', 'gray.600'];

  // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (
      request_type: RequestType,
      request_value: string | Blob,
  ) => {
    if (isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue.trim(),
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
        text: result.data.response! || "I'm sorry, I couldn't generate a response.",
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error calling endpoint:', err);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error while processing your message.",
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
    <Container maxW="4xl" h="100vh" p={0}>
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
              Parking Assistant Chat
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
                  Welcome to Parking Assistant! 🚗
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
                {/*  <Avatar size="sm" name="Assistant" bg="blue.500" />*/}
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
                  <Text>{message.text}</Text>
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
                {/* <Avatar size="sm" name="Assistant" bg="blue.500" /> */}
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

            <div ref={messagesEndRef} />
          </VStack>
        </Box>

        {/*<AudioRecorder*/}
        {/*  onRecordingComplete={(blob) => sendMessage(RequestType.VOICE_REQUEST, blob)}*/}
        {/*  audioTrackConstraints={{*/}
        {/*    noiseSuppression: true,*/}
        {/*    echoCancellation: true,*/}
        {/*  }}*/}
        {/*  downloadOnSavePress={false}*/}
        {/*/>*/}

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

            {(!recordingStatus || recordingStatus === "stopped") && (
              <IconButton
                  aria-label="Start Recording"
                  size="md"
                  onClick={startRecording}
              >
                <LuMic color="white" />
              </IconButton>
            )}

            {recordingStatus === "recording" && (
              <IconButton
                  aria-label="Start Recording"
                  size="md"
                  onClick={() => {
                    stopRecording((blob) => {
                      console.log("Recorded...");
                      sendMessage(RequestType.VOICE_REQUEST, blob!);
                    });
                  }}
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