

gcloud pubsub topics create cryptofeed

gcloud functions deploy crypto-feed --entry-point main --runtime python37 --trigger-resource cryptofeed --trigger-event google.pubsub.topic.publish --timeout 540s

gcloud scheduler jobs create pubsub cryptofeed_job --location us-west1 --schedule "*/10 * * * *" --topic cryptofeed --message-body "This is a job that I run twice per day!"











