from pathlib import Path
import tqdm
import json

import axelrod as axl

import pandas as pd

import sequence_sensei as ss


strategies = {
    strategy().name: strategy
    for strategy in axl.strategies
    if strategy.classifier["stochastic"] == True
}

genes = ["gene_{}".format(i) for i in range(205)]


def run_seed_match_with_repetitions(
    seed, player, sequence, score, repetitions=5
):
    for _ in range(repetitions):
        axl.seed(seed)
        match = axl.Match([player(), axl.Cycler(sequence)], turns=205)

        _ = match.play()

        check = score == match.final_score_per_turn()[-1]
        if check == False:
            return False
    return True


failed_names = []
checks = {}
for file in tqdm.tqdm(Path("/Volumes/ext/Data/raw_data/").glob("*")):
    file = str(file)
    if file.split("_")[-1] == "nan":
        continue
    df = pd.read_csv(file + "/main.csv")
    df = df[df["generation"] == 2000]

    for i, row in df[df["score"] == df["score"].max()].reset_index().iterrows():
        try:
            opponent = strategies[row["opponent"]]
        except KeyError:
            failed_names.append(row["opponent"])

        sequence = ss.get_sequence_str(row[genes].values)
        score = row["score"]
        seed = int(row["seed"])

        check = run_seed_match_with_repetitions(
            seed=seed, player=opponent, sequence=sequence, score=score
        )

        key = row["opponent"] + "_" + str(seed) + "_best_response_" + str(i)
        checks[key] = check

with open("checks.txt", "w") as file:
    file.write(json.dumps(checks))

with open("failed_names.txt", "w") as file:
    file.write("\n".join(failed_names))
