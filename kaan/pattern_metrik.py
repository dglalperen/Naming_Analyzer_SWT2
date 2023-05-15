from preprocessing_scripts import analyze_repository
from conventions import is_name_conformant


def calc_metrik(names_dict):
    total_names = 0
    total_conformant_names = 0
    for name_type, names in names_dict.items():
        total_names += len(names)
        total_conformant_names += sum(is_name_conformant(name, name_type) for name in names)
    return total_conformant_names / total_names if total_names > 0 else 0

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
    metric = calc_metrik(all_names)
    return metric




if __name__ == '__main__':

    token = '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'
    repo_url = 'https://github.com/donnemartin/system-design-primer'

    results = analyze_repository(repo_url, token)
    summary = summarize_results(results)
    print(summary)