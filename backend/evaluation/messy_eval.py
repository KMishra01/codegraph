test_set = [
    {"query": "how does causal self attention work", "correct_chunks": ["mingpt/model.py::CausalSelfAttention.forward"]},
    {"query": "where is the GPT model class defined", "correct_chunks": ["mingpt/model.py::GPT"]},
    {"query": "how are pretrained weights loaded", "correct_chunks": ["mingpt/model.py::GPT.from_pretrained"]},
    {"query": "how does text generation work", "correct_chunks": ["mingpt/model.py::GPT.generate"]},
    {"query": "how is the optimizer configured", "correct_chunks": ["mingpt/model.py::GPT.configure_optimizers (part 1)", "mingpt/model.py::GPT.configure_optimizers (part 2)"]},
    {"query": "how are model weights initialized", "correct_chunks": ["mingpt/model.py::GPT._init_weights"]},
    {"query": "what does the training loop look like", "correct_chunks": ["mingpt/trainer.py::Trainer.run"]},
    {"query": "how do you add a callback during training", "correct_chunks": ["mingpt/trainer.py::Trainer.add_callback"]},
    {"query": "how does byte pair encoding tokenization work", "correct_chunks": ["mingpt/bpe.py::Encoder.bpe (part 1)", "mingpt/bpe.py::Encoder.bpe (part 2)"]},
    {"query": "how is text encoded into tokens", "correct_chunks": ["mingpt/bpe.py::BPETokenizer.__call__"]},
    {"query": "how is a config object converted to a dictionary", "correct_chunks": ["mingpt/utils.py::CfgNode.to_dict"]},
    {"query": "how do you set a random seed for reproducibility", "correct_chunks": ["mingpt/utils.py::set_seed"]},
    {"query": "how does the addition dataset generate training examples", "correct_chunks": ["projects/adder/adder.py::AdditionDataset.__getitem__"]},
    {"query": "what is the GELU activation implementation", "correct_chunks": ["mingpt/model.py::NewGELU.forward"]},
    {"query": "how does a transformer block combine attention and mlp", "correct_chunks": ["mingpt/model.py::Block.forward"]},
    {"query": "how does the tokenizer merge byte pairs together", "correct_chunks": ["mingpt/bpe.py::Encoder.bpe (part 1)", "mingpt/bpe.py::Encoder.bpe (part 2)"]},
    {"query": "how does encoding show its intermediate steps", "correct_chunks": ["mingpt/bpe.py::Encoder.encode_and_show_work"]},
    {"query": "how are tokens converted back into text", "correct_chunks": ["mingpt/bpe.py::Encoder.decode"]},
    {"query": "how does the tokenizer download or cache its vocab files", "correct_chunks": ["mingpt/bpe.py::get_file"]},
    {"query": "how do you build the byte pair encoder from vocab and merges", "correct_chunks": ["mingpt/bpe.py::get_encoder"]},
    {"query": "how does a config value get overridden from command line args", "correct_chunks": ["mingpt/utils.py::CfgNode.merge_from_args"]},
    {"query": "how does a config object print itself readably", "correct_chunks": ["mingpt/utils.py::CfgNode.__str__"]},
    {"query": "how is training progress logged to a folder", "correct_chunks": ["mingpt/utils.py::setup_logging"]},
    {"query": "how does the addition dataset know its vocabulary size", "correct_chunks": ["projects/adder/adder.py::AdditionDataset.get_vocab_size"]},
    {"query": "how does the character dataset turn text into training examples", "correct_chunks": ["projects/chargpt/chargpt.py::CharDataset.__getitem__"]},

    {"query": "how is masking applied in attention", "correct_chunks": ["mingpt/model.py::CausalSelfAttention.forward"]},

{"query": "how are attention scores computed", "correct_chunks": ["mingpt/model.py::CausalSelfAttention.forward"]},

{"query": "how are query key value matrices created", "correct_chunks": ["mingpt/model.py::CausalSelfAttention.forward"]},

{"query": "how does residual connection work in transformer block", "correct_chunks": ["mingpt/model.py::Block.forward"]},

{"query": "how is layer normalization applied in transformer block", "correct_chunks": ["mingpt/model.py::Block.forward"]},
{"query": "how are logits converted to probabilities during generation", "correct_chunks": ["mingpt/model.py::GPT.generate"]},

{"query": "how does sampling from probability distribution work", "correct_chunks": ["mingpt/model.py::GPT.generate"]},

{"query": "how is temperature used in text generation", "correct_chunks": ["mingpt/model.py::GPT.generate"]},

{"query": "how does top k sampling work", "correct_chunks": ["mingpt/model.py::GPT.generate"]},
{"query": "how is loss computed during training", "correct_chunks": ["mingpt/model.py::GPT.forward"]},

{"query": "how are gradients updated during training", "correct_chunks": ["mingpt/trainer.py::Trainer.run"]},

{"query": "how often is evaluation run during training", "correct_chunks": ["mingpt/trainer.py::Trainer.run"]},

{"query": "how is batch processed in training loop", "correct_chunks": ["mingpt/trainer.py::Trainer.run"]},
{"query": "how are unknown tokens handled in tokenizer", "correct_chunks": ["mingpt/bpe.py::Encoder.encode"]},

{"query": "how does tokenizer handle whitespace", "correct_chunks": ["mingpt/bpe.py::Encoder.encode"]},

{"query": "how are tokens mapped to integer ids", "correct_chunks": ["mingpt/bpe.py::Encoder.encode"]},
]