from transformers import PreTrainedModel, PreTrainedTokenizer, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


from safe_llm_finetune.fine_tuning.base import ModelAdapter 


class GemmaAdapter(ModelAdapter):
    """Adapter for google/gemma-3-1B-it model."""
    
    def __init__(self, model_name="google/gemma-3-1B-it"):
        super().__init__(model_name)
    
    def load_model(self) -> PreTrainedModel:
        """
        Load the Gemma model from HuggingFace.
            
        Returns:
            Loaded model
        """
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            attn_implementation='eager',
            trust_remote_code=True
        )
        return model
    
    def load_tokenizer(self) -> PreTrainedTokenizer:
        """
        Load the Gemma tokenizer from HuggingFace.
            
        Returns:
            Loaded tokenizer
        """
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        return tokenizer
    
    def load_quantized_model(self, quantization_config: BitsAndBytesConfig) -> PreTrainedModel:
        """ Load a model from HuggingFace in specified quantization

        Args:
            quantization_config (BitsAndBytesConfig): config for quantization

        Returns:
            PreTrainedModel: model loaded in specified quantization
        """
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True
        )
        return model
    
    
    def get_name(self):
        """
        Returns name of model
        """
        return "gemma-3-1B-it"
    
    def get_available_modules(self):
        """
        Returns all available modules that can be targeted for fine-tuning in Gemma
        """
        # All potential target modules in Gemma model
        return {
            # Attention modules
            "attention": ["q_proj", "k_proj", "v_proj", "o_proj"],
            # MLP modules
            "mlp": ["gate_proj", "up_proj", "down_proj"],
            # Layer norms
            "layer_norms": ["input_layernorm", "post_attention_layernorm"]
        }
    
    def get_lora_modules(self):
        available = self.get_available_modules()
        # Most efficient default for LoRA: focus on query and key projections
        return ["q_proj", "k_proj"]
    
    def get_qlora_modules(self):
        available = self.get_available_modules()
        # QLoRA often includes more modules: attention + MLP
        return available["attention"] + available["mlp"]