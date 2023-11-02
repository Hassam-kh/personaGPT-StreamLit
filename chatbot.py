from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
path = "af1tang/personaGPT"
tokenizer = GPT2Tokenizer.from_pretrained(path, padding_side='left')
model = GPT2LMHeadModel.from_pretrained(path)
def flatten(l): return [item for sublist in l for item in sublist]


def to_data(x):
    if torch.cuda.is_available():
        x = x.cpu()
    return x.data.numpy()


def to_var(x):
    if not torch.is_tensor(x):
        x = torch.Tensor(x)
    if torch.cuda.is_available():
        x = x.cuda()
    return x


def display_dialog_history(dialog_hx):
    for j, line in enumerate(dialog_hx):
        msg = tokenizer.decode(line)
        if j % 2 == 0:
            print(">> User: " + msg)
        else:
            print(">> Bot: "+msg)
            print()


def generate_next(bot_input_ids, do_sample=True, top_k=10, top_p=.92, max_length=1000, pad_token=tokenizer.eos_token_id):
    full_msg = model.generate(bot_input_ids, do_sample=True,
                              top_k=top_k, top_p=top_p,
                              max_length=max_length, pad_token_id=tokenizer.eos_token_id)
    msg = to_data(full_msg.detach()[0])[bot_input_ids.shape[-1]:]
    return msg


def chatting_conv(val, transcription, dialog_hx):
    personas = [
        f"Given the instructions by User to bot, the bot has to abide by these rules and instruction, also never go astray from the instructions provided by User {tokenizer.eos_token}."]
    val += tokenizer.eos_token
    personas.append(val)
    personas = tokenizer.encode(
        ''.join(['<|p2|>'] + personas + ['<|sep|>'] + ['<|start|>']))
    user_inp = tokenizer.encode(
        ">> User: " + transcription.strip() + tokenizer.eos_token)
    bot_input_ids = to_var([personas + flatten(dialog_hx)]).long()
    msg = generate_next(bot_input_ids)
    return str(("Bot: {}".format(tokenizer.decode(msg, skip_special_tokens=True)))), user_inp, msg, tokenizer.decode(user_inp), tokenizer.decode(msg)
