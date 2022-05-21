

gcloud pubsub topics create cryptofeed

gcloud functions deploy crypto-feed --entry-point main --runtime python37 --trigger-resource cryptofeed --trigger-event google.pubsub.topic.publish --timeout 540s --env-vars-file .env.yaml

gcloud scheduler jobs create pubsub cryptofeed_job --location us-west1 --schedule "*/10 * * * *" --topic cryptofeed --message-body "This is a job that I run twice per day!"

gcloud dataflow jobs run reader-crypto-live --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery --region us-east1 --staging-location gs://datalake_crypto_feed/tmp/ --parameters "inputTopic=projects/your-project-id/topics/sales,outputTableSpec=your-project-id:ds_crypto_monitoring.stg_crypto_live"


terraform init 

terraform validate

terraform plan

terraform apply









