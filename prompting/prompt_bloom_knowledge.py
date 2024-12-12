import json

from datasets import tqdm, load_dataset

from direct.direct import DirectPrompt

with open('classify_knowledge_prompt_demonstrations_gpt.txt', 'r') as f:
    prompt_original = f.read()

direct = DirectPrompt(
    model='gpt-4',
    # max_tokens=100
)
dataset = 'maveriq/bigbenchhard'
# load dataset from huggingface
configs = ['boolean_expressions', 'causal_judgement', 'date_understanding', 'disambiguation_qa', 'dyck_languages',
           'formal_fallacies', 'geometric_shapes', 'hyperbaton', 'logical_deduction_five_objects',
           'logical_deduction_seven_objects', 'logical_deduction_three_objects', 'movie_recommendation',
           'multistep_arithmetic_two', 'navigate', 'object_counting', 'penguins_in_a_table',
           'reasoning_about_colored_objects', 'ruin_names', 'salient_translation_error_detection', 'snarks',
           'sports_understanding', 'temporal_sequences', 'tracking_shuffled_objects_five_objects',
           'tracking_shuffled_objects_seven_objects', 'tracking_shuffled_objects_three_objects', 'web_of_lies',
           'word_sorting']
out = {}
for config in tqdm(configs, desc='Classifying BigBenchHard - Cognitive', total=len(configs)):
    data = load_dataset(dataset, config, cache_dir=None)
    outputs = []
    for sample in data['train'][:10]['input']:
        prompt = prompt_original.replace('{problem}', sample)
        output = direct.do_prompting(prompt)
        outputs.append(output)
    out[config] = outputs

with open('bbh_predictions/bigbenchhard_predictions_knowledge_gpt4_10.json', 'w') as f:
    json.dump(out, f)