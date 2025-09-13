import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  Flex,
  Text,
  // keyframes
} from '@chakra-ui/react';
import { Play, Pause } from 'lucide-react';

// Define pulse animation for Chakra UI
// const pulse = keyframes`
//   0%, 100% { opacity: 1; }
//   50% { opacity: 0.5; }
// `;

const VoiceMessageComponent = ({ audioBlob, duration = 30 }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [audioDuration, setAudioDuration] = useState(duration);
  const [isLoading, setIsLoading] = useState(true);
  const audioRef = useRef(null);
  const audioUrl = useRef(null);

  // Color mode values
  const bgColor = ['gray.800', 'gray.700'];
  const buttonBg = ['white', 'gray.100'];
  const buttonHoverBg = ['gray.100', 'gray.200'];
  const iconColor = ['gray.800', 'gray.800'];
  const textColor = ['white', 'gray.100'];
  const inactiveBarColor = ['gray.600', 'gray.500'];
  const activeBarColor = ['white', 'gray.100'];

  // Generate waveform bars (you can replace this with actual audio analysis)
  const generateWaveform = () => {
    const bars = [];
    for (let i = 0; i < 60; i++) {
      const height = Math.random() * 20 + 5; // Random height between 5-25px
      bars.push(height);
    }
    return bars;
  };

  const [waveformBars] = useState(generateWaveform());

  useEffect(() => {
    if (audioBlob) {
      // Create URL from blob
      audioUrl.current = URL.createObjectURL(audioBlob);

      // Clean up URL when component unmounts
      return () => {
        if (audioUrl.current) {
          URL.revokeObjectURL(audioUrl.current);
        }
      };
    }
  }, [audioBlob]);

  useEffect(() => {
    audioUrl.current = URL.createObjectURL(audioBlob);
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => {
      setAudioDuration(audio.duration);
      setIsLoading(false);
    }
    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);
    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);

      if (audioUrl.current) {
          URL.revokeObjectURL(audioUrl.current);
      }
    };
  }, [audioBlob]);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio || !audioUrl.current) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const progress = audioDuration > 0 ? (currentTime / audioDuration) * 100 : 0;

  return (
    <Flex
      align="center"
      gap={3}
      p={4}
      bg={bgColor}
      borderRadius="2xl"
      maxW="md"
    >
      {/* Audio element */}
      <audio
        ref={audioRef}
        src={audioUrl.current}
        preload="metadata"
      />

      {/* Play/Pause Button */}
      {isLoading && (<Button
        onClick={togglePlayPause}
        disabled
        w={10}
        h={10}
        minW={10}
        bg={buttonBg}
        _hover={{ bg: buttonHoverBg }}
        _disabled={{
          opacity: 0.5,
          cursor: 'not-allowed'
        }}
        borderRadius="full"
        p={0}
        display="flex"
        alignItems="center"
        justifyContent="center"
        transition="background-color 0.2s"
      >
        {isPlaying ? (
          <Pause size={16} style={{ marginLeft: '0.125rem' }} />
        ) : (
          <Play size={16} style={{ marginLeft: '0.125rem' }} />
        )}
      </Button>)}

      {!isLoading && (<Button
        onClick={togglePlayPause}
        w={10}
        h={10}
        minW={10}
        bg={buttonBg}
        _hover={{ bg: buttonHoverBg }}
        _disabled={{
          opacity: 0.5,
          cursor: 'not-allowed'
        }}
        borderRadius="full"
        p={0}
        display="flex"
        alignItems="center"
        justifyContent="center"
        transition="background-color 0.2s"
      >
        {isPlaying ? (
          <Pause size={16} style={{ marginLeft: '0.125rem' }} />
        ) : (
          <Play size={16} style={{ marginLeft: '0.125rem' }} />
        )}
      </Button>)}

      {/* Waveform */}
      <Flex
        align="center"
        gap="1px"
        flex={1}
        h={8}
        position="relative"
        overflow="hidden"
      >
        {waveformBars.map((height, index) => {
          const barProgress = (index / waveformBars.length) * 100;
          const isActive = barProgress <= progress;

          return (
            <Box
              key={index}
              w="2px"
              borderRadius="full"
              transition="all 0.15s"
              bg={isActive ? activeBarColor : inactiveBarColor}
              animation={isPlaying && isActive ? `animate-pulse 1s ease-in-out infinite` : undefined}
              style={{
                height: `${height}px`,
                animationDelay: `${index * 50}ms`
              }}
            />
          );
        })}
      </Flex>

      {/* Duration */}
      <Text
        color={textColor}
        fontSize="sm"
        fontFamily="mono"
        minW="max-content"
        whiteSpace="nowrap"
      >
        {formatTime(currentTime)} / {formatTime(audioDuration)}
      </Text>
    </Flex>
  );
};

export default VoiceMessageComponent;