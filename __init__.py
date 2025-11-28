# This file tells ComfyUI to load the nodes from sts_node.py
from .sts_node import ElevenLabs_SpeechToSpeech

# This maps the node's class name to its display name
NODE_CLASS_MAPPINGS = {
    "ElevenLabs_SpeechToSpeech": ElevenLabs_SpeechToSpeech
}

# This is the name that will show up in the "Add Node" menu
NODE_DISPLAY_NAME_MAPPINGS = {
    "ElevenLabs_SpeechToSpeech": "ElevenLabs Speech-to-Speech"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']