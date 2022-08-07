DROP TABLE IF EXISTS dialogs;

CREATE TABLE dialogs (
  customer_id INTEGER NOT NULL,
  dialog_id INTEGER NOT NULL,
  dialog_text TEXT NOT NULL,
  dialog_language TEXT NOT NULL,
  dialog_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dialogs (customer_id, dialog_id, dialog_text, dialog_language, dialog_timestamp)
VALUES
(1, 1, 'Text 11', 'en', '2022-08-08 00:00:00.000000'),
(1, 2, 'Text 12', 'en', '2022-08-08 00:01:00.000000'),
(2, 1, 'Text 21', 'en', '2022-08-08 00:02:00.000000'),
(3, 1, 'Text 31', 'de', '2022-08-08 00:03:00.000000');