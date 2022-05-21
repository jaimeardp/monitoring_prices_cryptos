resource "google_bigquery_dataset" "default" {
  dataset_id                  = "ds_crypto_monitoring_tf"
  project                     = "${var.prodproject}"
  friendly_name               = "people"
  description                 = "Dataset for crypto tables"
  location                    = "US"
  labels ={
    env = "default"
  }
}
resource "google_bigquery_table" "default" {
  dataset_id = "${google_bigquery_dataset.default.dataset_id}"
  project    = "${var.prodproject}"
  table_id   = "stg_crypto_live"
  time_partitioning {
    type = "DAY"
  }
  labels ={
    env = "default"
  }
  schema = "${file("${path.module}/schema.json")}"
}

resource "google_logging_metric" "logging_metric" {
  project    = "${var.prodproject}"
  count = length(var.currencies_names)
  name   = "metrica_dist_monitoring_crypto_price_${var.currencies_names[count.index]}"
  filter = "logName: monitoring_crypto_price_${var.currencies_names[count.index]} labels.type = product"
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "DISTRIBUTION"
    unit        = "1"
    display_name = "metrica_dist_monitoring_crypto_price_${var.currencies_names[count.index]}"
  }
  value_extractor = "EXTRACT(jsonPayload.stock)"
  bucket_options {
    linear_buckets {
      num_finite_buckets = 3
      width              = 1
      offset             = 1
    }
  }
}