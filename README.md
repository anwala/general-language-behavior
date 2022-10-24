# A General Language for Modeling Social Media Account Behavior

This repository contains code and data required to replicate the results from the paper, [A General Language for Modeling Social Media Account Behavior](#).

## BOT DETECTION

We compared the performance of BLOC to three baselines, [Botometer](https://botometer.osome.iu.edu/), [Twitter DNA](https://doi.org/10.1109/TDSC.2017.2681672), and [DNA-influenced](https://www.nature.com/articles/s41598-022-11854-w) on the bot detection task. Here we provide the references to all the methods excluding Botometer since its code is not publicly available.

#### Dataset
All tweets and accounts used in the bot detection task can be found in the [Bot repository dataset](https://botometer.osome.iu.edu/bot-repository/datasets.html).

#### Models
  * BLOC
  * Twitter DNA
  * DNA-Influenced

####  Evaluate BLOC
  0. [Install BLOC](https://github.com/anwala/bloc)
  1. Set `RAW_TRAINING_DATA_ROOT` in [`general-language-behavior/bot-detect/bloc-eval/workflow/Snakefile`](https://github.com/anwala/general-language-behavior/blob/main/bot-detect/eval-bloc/workflow/Snakefile#L25) with the path to the evaluation dataset consisting of the `tweets.jsons.gz`
  2. Set `TARGET_ROOT` in [`general-language-behavior/bot-detect/bloc-eval/workflow/Snakefile`](https://github.com/anwala/general-language-behavior/blob/main/bot-detect/eval-bloc/workflow/Snakefile#L32) with the output path (e.g., `/tmp/bot-detect-res/`) for the evaluation results. Then run the following commands.
  3. `$ conda activate snakemake`
  4. `$ cd general-language-behavior/bot-detect/bloc-eval/workflow`
  5. `$ snakemake --cores=5 run_ml_all`
  6. The f1, recall, precision, and number of features are written to the `ml_results_all.cvs` file in the output path (e.g., `/tmp/bot-detect-res/ml_results_all.csv`). 
  To reset experiment, delete all content from output path (e.g., `$rm -rf /tmp/bot-detect-res/*`), then run `$ snakemake --cores=5 run_ml_all`

#### Evaluate Twitter DNA and DNA-Influenced
  0. Install Twitter DNA:
  ```bash
  $ pip install -r general-language-behavior/bot-detect/eval-dna/requirements.txt
  $ pip general-language-behavior/bot-detect/eval-dna/ddna-toolbox/glcr/
  $ pip general-language-behavior/bot-detect/eval-dna/ddna-toolbox/
  ```
  1. [Install BLOC](https://github.com/anwala/bloc)
  2. Run the following command, and ensure to set `--tweets-path` with the path to the tweets dataset.
  ```bash
    $ python general-language-behavior/bot-detect/eval-dna/bloc_paper.py --max-users=200 --evaluate-models sf sf-influenced --tweets-path=/path/to/bot_repo_tweets --task evaluate verified kevin_feedback pronbots stock rtbust midterm-2018 zoher-organization botwiki gilani-17 varol-icwsm gregory_purchased astroturf cresci-17 josh_political
  ```
  3. The evaluation results are written into `./bot_detection_results.json`

## COORDINATION DETECTION

We compared the performance of BLOC with three baselines, Activity, Co-retweet (CoRT), and Hashtag (Hash), in the coordination detection task. All models are implemented in the [Twitter Infoops Toolkit](https://github.com/anwala/twitter-infoops-toolkit)

#### Dataset 
The drivers and their tweets can be downloaded from the [Twitter Information Operations dataset](https://transparency.twitter.com/en/reports/moderation-research.html#1.3). Next, we describe the steps for creating the control dataset.

#### Create control dataset
See the [Twitter Info Ops toolkit documentation](https://github.com/anwala/twitter-infoops-toolkit#create-control-dataset) on how to create tweets (stored in `DriversControl/control_driver_tweets.jsonl.gz`) for control users.

#### Evaluate coordination detection methods

Consider this example to evaluate all methods for a campaign (e.g., `armenia_202012`). The file containing the driver tweets must be named `driver_tweets.csv.gz` and the `DriverControl` folder which contains the control dataset must reside in the same location as `driver_tweets.csv.gz`. 
```bash
$ ls `/tmp/armenia_202012`
DriversControl  driver_tweets.csv.gz
```
The following command evaluates BLOC and the baseline coordination detection methods for the first weeks of the life cycle of the drivers. Use `--knn-reverse-dates` to run the evaluation for the last weeks of the life cycle of drivers. The syntax is strict, so mimic the following command closely. 
```bash
$ ops --task=knn_classify_bloc_drivers_vs_drivers_control --tweets-path=/tmp/ armenia_202012/driver_tweets.csv.gz
```

The evaluation result for each model (e.g., BLOC) would be written to `Twitter_InfoOps_Output`. For example, `Twitter_InfoOps_Output/eval/drivers_v_control/knn/k-first-active-years/bloc_armenia_202012.json`
