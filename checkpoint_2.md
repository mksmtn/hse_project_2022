# Checkpoint 2

[Файлы в Dropbox](https://www.dropbox.com/scl/fo/948ljzrtu2zltpv1tiuf5/h?dl=0&rlkey=0okbfzdgkvsjhy3iouhhdgheq)

В папке есть архив `fma_large.zip`, в котором обрезки треков по 30 секунд. Быть может, мы будем делать какой-то анализ не на обрывках, а на целых треках, но тут прошу понять и простить, файл в 879ГБ загружать в Dropbox, да и скачивать пока себе на комп, не стал. Вместо этого, его можно скачать [по ссылке](https://os.unil.cloud.switch.ch/fma/fma_full.zip). Он имеет аналогичную структуру, что и `fma_large.zip`, нео треки представлены целиком. Подробнее [в официальном репозитории FMA](https://github.com/mdeff/fma).

В Dropbox залиты два датасета, [Last.fm two billion events](http://www.cp.jku.at/datasets/LFM-2b/) и [Free Music Archive](https://github.com/mdeff/fma). LFM-2b больше подходит для рекомендаций треков пользователям по их истории прослушиваний, а FMA для анализа аудиофайлов, например для предсказания жанра по аудио.

В папке `lfm-b2` следующие файлы:

1. `albums.tsv` с колонками: album_id, album_name, artist_name;

2. `artists.tsv` с колонками: artist_id, artist_name;

3. `listening-events.tsv` с колонками: user_id, track_id, album_id, timestamp;

4. `tracks.tsv` с колонками: track_id, artist_name, track_name;

5. `listening-counts.tsv` с колонками: user_id, track_id, count;

6. `users.tsv` с колонками: user_id, country, age, gender, creation_time;

7. `tags.json`и `tags-micro-genres.json` имеют аналогичную структуру. В них каждая строчка представляет из себя отдельный json формата: `{"_id": {"artist": "имя артиста", "track": "название трека"}, "tags": {"какой-то тэг": 100, "другой тэг": 90}, "i": 123}`, где *i* — id трэка, а в *tags* является объектом, где ключ — название тэга, а значение — вес тэга. Разница в том, что в `tags.json` лежат тэги, добавленные пользователями, и там куча всякого мусора типа `"overrated":1,"Rolling":1,"paul epworth":1,"straight to the heart":1,"damned good":1,"Soundtrack Of My Life":1,"powerful vocal":1,"teenage love between the sheets":1,"christian alexander tietgen":1,"fuck you for breaking my heart":1`.

В файле `fma_large.zip` заархивирована папка `fma_large`, в которой лежат файлы `README.txt`, `checksums` и папки с названиями из трёх цифр от `000` до `155`. Каждая из папок содержит трэки с айдишниками, начинающимися с соответсвующих чисел, например в папке `154` лежат файлы `154000.mp3`, ..., `154999.mp3`. В папке `155` последний трэк `155320.mp3`. Название трэка является его айдишником.

В папке `fma_metadata` содержатся данные о исполнителях и названиях трэков, ассоциированные с айдишниками трэков, используемых в аудиофайлах и другие данные:

1. `raw_tracks.csv` с колонками: track_id,album_id,album_title,album_url,artist_id,artist_name,artist_url,artist_website,license_image_file,license_image_file_large,license_parent_id,license_title,license_url,tags,track_bit_rate,track_comments,track_composer,track_copyright_c,track_copyright_p,track_date_created,track_date_recorded,track_disc_number,track_duration,track_explicit,track_explicit_notes,track_favorites,track_file,track_genres,track_image_file,track_information,track_instrumental,track_interest,track_language_code,track_listens,track_lyricist,track_number,track_publisher,track_title,track_url

2. `genres.csv` с колонками: genre_id,#tracks,parent,title,top_level

3. Есть другие файлы, но пока их использовать не планируем. Например, `tracks.csv`. Непонятна его структура, кажется `raw_tracks.csv` будет достаточно.
