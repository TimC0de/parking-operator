from openai import OpenAI


class AudioTranscriber:

    def __init__(self, client: OpenAI):
        self.client = client

    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper

        Args:
            audio_file_path (str): Path to the audio file

        Returns:
            str: Transcribed text
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript.strip()
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"
