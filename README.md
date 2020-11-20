# botfront-example
This is botfront example project, in which we try 
to add new rasa-components and rasa-actions. 

### Build docker image for ner-service
To use the `custom_entities` in the rasa pipeline, you need to build
another docker image using- https://github.com/patelrajnath/ner_service

### Run the botfront project
```bash
$git clone https://github.com/patelrajnath/botfront-example.git
$cd botfront-example
## Start all the services
$botfront up
```

Now, the front-end will be accessible at- http://localhost:8888/

### Pipeline with custom classifier
```json
pipeline:
  - name: WhitespaceTokenizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: flask_serving_classifier
  - name: rasa_addons.nlu.components.gazette.Gazette
  - name: >-
      rasa_addons.nlu.components.intent_ranking_canonical_example_injector.IntentRankingCanonicalExampleInjector
  - name: EntitySynonymMapper
```

### Pipeline with custom ner+classifier
```json
pipeline:
  - name: WhitespaceTokenizer
  - name: RemoteSpacyCustomNER
    dropout: 0.1
    accumulate_gradient: 1
    patience: 100
    max_epochs: 0
    max_steps: 500
    eval_frequency: 100
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: flask_serving_classifier
  - name: rasa_addons.nlu.components.gazette.Gazette
  - name: >-
      rasa_addons.nlu.components.intent_ranking_canonical_example_injector.IntentRankingCanonicalExampleInjector
  - name: EntitySynonymMapper
```

**Note**: The classifier is integrated as remote service 
(disable the VPN if any). Make sure that the service is running at-
```json
host = '185.190.206.134'
port = 9000
```

We can also confirm the same using curl-
```bash
$curl curl 185.190.206.134:9000/train
```
The expected output is- `{"message": {"text": "No text provided"}}`
