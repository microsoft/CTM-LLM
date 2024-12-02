import argparse
import json
from pprint import pprint
from functools import reduce


def load_jsons(x):
  with open(x, 'r') as f:
      return [json.loads(line) for line in f]

def norm_list(x):
  if not x:
    return None
  return json.dumps(sorted(x))

def norm_ground_truth(x):
  return (x['NCT_ID'], x['histology_inclusion_norm'], norm_list(x['biomarker_inclusion_norm']), norm_list(x['histology_exclusion_norm']), norm_list(x['biomarker_exclusion_norm']))

def norm_pred(x, ground_truth_nct_ids):
  nct_id, data_list = x['NCT_id'], x['json_norm']
  result = []
  if not data_list:
    return result
  if nct_id not in ground_truth_nct_ids:
    return []
  for data in data_list:
    result.append((nct_id, data.get('histology_inclusion', None), norm_list(data.get('biomarker_inclusion', None)), norm_list(data.get('histology_exclusion', None)), norm_list(data.get('biomarker_exclusion', None))))
  return result

def eval(pred, ground_truth):
  recall = len(pred&ground_truth)/len(ground_truth)*100
  precision = len(pred&ground_truth)/len(pred)*100 if len(pred) else 0
  f1 = 2*recall*precision/(recall+precision) if recall+precision else 0
  print(f"Recall: {recall:.1f}")
  print(f"Precision: {precision:.1f}")
  print(f"F1: {f1:.1f}")
  return {'Recall': f"{recall:.1f}", 'Precision': f"{precision:.1f}", 'F1': f"{f1:.1f}"}

def get_hist_incl(data):
	"""Filter histology inclusion relations"""
	return set((x[0], x[1]) for x in data if x[1])

def get_hist_incl_excl(data):
  """Filter histology inclusion and exclusion relations"""
  return set((x[0], x[1], x[3]) for x in data if x[1] or x[3])

def get_biom_incl(data):
  """Filter biomarker inclusion relations"""
  return set((x[0], x[2]) for x in data if x[2])

def get_biom_incl_no_logic(data):
  """Filter biomarker inclusion relations (Ignore Logic)"""
  return set((x[0], json.dumps(biom)) for x in data if x[2] for biom in json.loads(x[2]))

def get_biom_incl_excl(data):
  """Filter biomarker inclusion and exclusion relations"""
  return set((x[0], x[2], x[4]) for x in data if x[2] or x[4])

def get_hist_biom_incl(data):
  """Filter histology and biomarker inclusion relations"""
  return set((x[0], x[1], x[2]) for x in data if x[1] or x[2])

def get_biom_incl_excl_no_logic(data):
  """Filter biomarker inclusion and exclusion relations (Ignore Logic)"""
  incl_set = set((x[0], json.dumps(biom), True) for x in data  if x[2] for biom in json.loads(x[2]))
  excl_set = set((x[0], json.dumps(biom), False) for x in data  if x[4] for biom in json.loads(x[4]))
  return incl_set|excl_set

def get_histology_incl_excl_no_logic(data):
  incl_set = set((x[0], x[1], True) for x in data if x[1])
  excl_set = set((x[0], biom, False) for x in data  if x[3] for biom in json.loads(x[3]))
  return incl_set|excl_set


def main(args):
  result = {}
  print(f"Input Prediction Path: {args.input_pred_path}")
  print(f"Input Ground Truth Path: {args.input_ground_truth_path}")
  
  ground_truth_raw_relations = load_jsons(args.input_ground_truth_path)
  ground_truth_relations_set = set(map(norm_ground_truth, ground_truth_raw_relations))
  ground_truth_nct_ids = set(x['NCT_ID'] for x in ground_truth_raw_relations)
  
  pred_raw_relations = load_jsons(args.input_pred_path)
  pred_relations_set = map(lambda x:norm_pred(x, ground_truth_nct_ids), pred_raw_relations)
  pred_relations_set = set(reduce(list.__add__, pred_relations_set))
  
  result['total_pred_rels'] = len(pred_relations_set)
  result['total_ground_truth_rels'] = len(ground_truth_relations_set)
  
  print(f"Total Predicted Relations: {len(pred_relations_set)}")
  print(f"Total Ground Truth Relations: {len(ground_truth_relations_set)}")
  
  # Evaluate Histology Biomarker Inclusion Exclusion (Exact Relation)
  result_dict = eval(pred_relations_set, ground_truth_relations_set)
  result['hist_biom_incl_excl'] = result_dict
  
  # Evaluate Histology Inclusion
  pred_hist_incl_set = get_hist_incl(pred_relations_set)
  ground_truth_hist_incl_set = get_hist_incl(ground_truth_relations_set)
  result_dict = eval(pred_hist_incl_set, ground_truth_hist_incl_set)
  result['hist_incl'] = result_dict
  
  # Evaluate Histology Inclusion Exclusion
  pred_hist_incl_excl_set = get_hist_incl_excl(pred_relations_set)
  ground_truth_hist_incl_excl_set = get_hist_incl_excl(ground_truth_relations_set)
  result_dict = eval(pred_hist_incl_excl_set, ground_truth_hist_incl_excl_set)
  result['hist_incl_excl'] = result_dict
 	
  # Evaluate Biomarker Inclusion
  pred_biom_incl_set = get_biom_incl(pred_relations_set)
  ground_truth_biom_incl_set = get_biom_incl(ground_truth_relations_set)
  result_dict = eval(pred_biom_incl_set, ground_truth_biom_incl_set)
  result['biomarker_incl'] = result_dict
  
  # Evaluate Biomarker Inclusion (Ignore Logic)
  pred_biom_incl_nl_set = get_biom_incl_no_logic(pred_relations_set)
  ground_truth_biom_incl_nl_set = get_biom_incl_no_logic(ground_truth_relations_set)
  result_dict = eval(pred_biom_incl_nl_set, ground_truth_biom_incl_nl_set)
  result['biomarker_incl_no_logic'] = result_dict
  
  # Evaluate Biomarker Inclusion Exclusion
  pred_biom_incl_excl_set = get_biom_incl_excl(pred_relations_set)
  ground_truth_biom_incl_excl_set = get_biom_incl_excl(ground_truth_relations_set)
  result_dict = eval(pred_biom_incl_excl_set, ground_truth_biom_incl_excl_set)
  result['biomarker_incl_excl'] = result_dict
  
  # Evaluate Histology + Biomarker Inclusion
  pred_hist_biom_incl_set = get_hist_biom_incl(pred_relations_set)
  ground_truth_hist_biom_incl_set = get_hist_biom_incl(ground_truth_relations_set)
  result_dict = eval(pred_hist_biom_incl_set, ground_truth_hist_biom_incl_set)
  result['histology_biomarker_incl'] = result_dict
  
  # Evaluate Biomarker Inclusion Exclusion (Ignore Logic)
  pred_biom_incl_set = get_biom_incl_excl_no_logic(pred_relations_set)
  ground_truth_biom_incl_set = get_biom_incl_excl_no_logic(ground_truth_relations_set)
  result_dict = eval(pred_biom_incl_set, ground_truth_biom_incl_set)
  result['biomarker_incl_excl_no_logic'] = result_dict
  
  # Evaluate Biomarker Inclusion Exclusion (Ignore Logic)
  pred_hist_set = get_histology_incl_excl_no_logic(pred_relations_set)
  ground_truth_hist_set = get_histology_incl_excl_no_logic(ground_truth_relations_set)
  result_dict = eval(pred_hist_set, ground_truth_hist_set)
  result['histology_incl_excl_no_logic'] = result_dict
  
  pprint(result)
  return result
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument('--input_pred_path', type=str, required=True, help='Path to the prediction file')
    parser.add_argument('--input_ground_truth_path', type=str, required=True, help='Path to the ground truth file')
    
    args = parser.parse_args()
    main(args)