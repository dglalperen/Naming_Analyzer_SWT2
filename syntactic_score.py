from preprocessing_scripts import analyze_repository
from syntactic import is_name_conformant


def calc_metrik(names_dict):
    total_names = 0
    total_conformant_names = 0
    non_conformant_names = {
        "function": [],
        "class": [],
        "variable": [],
        "constant": []
    }

    for name_type, names in names_dict.items():
        total_names += len(names)
        for name in names:
            if is_name_conformant(name, name_type):
                total_conformant_names += 1
            else:
                non_conformant_names[name_type].append(name)

    metric = total_conformant_names / total_names if total_names > 0 else 0
    return metric, non_conformant_names

def summarize_results(results):
    all_names = {
        "function": [],
        "class": [],
        "variable": [],
        "constant": []
    }
    for result in results:
        for name_type in all_names.keys():
            all_names[name_type].extend(result.get(name_type, []))
    return all_names



def rate_repository_syntactic(repo_name):

    results = analyze_repository(repo_name)
    summary = summarize_results(results)
    metric, non_conformant_names = calc_metrik(summary)
    return metric



if __name__ == '__main__':

    token = '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'
    repo_url = 'https://github.com/vfaronov/httpolice'

    metric, non_conformant_names = rate_repository_syntactic(repo_url, token)