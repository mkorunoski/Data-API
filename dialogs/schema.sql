DROP TABLE IF EXISTS dialogs;

CREATE TABLE dialogs (
  customer_id INTEGER NOT NULL,
  dialog_id INTEGER NOT NULL,
  dialog_text TEXT NOT NULL,
  dialog_language TEXT NOT NULL,
  dialog_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
