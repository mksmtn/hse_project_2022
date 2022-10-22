from functools import reduce
from typing import Iterable, Tuple


def get_genre(tags_data):
    genres: dict = tags_data['tags']
    return reduce(lambda acc, item: item if item[1] > acc[1] else acc, genres.items())[0]


class TrackListeningCount:
    def __init__(self, line: str) -> None:
        _, track_id, count = line.split()
        self.track_id = track_id
        self.count = int(count)


def count_track_listenings(track_listening_counts: Iterable[TrackListeningCount]):
    track_listening_count_map = dict()
    for listening_count in track_listening_counts:
        track_id = listening_count.track_id
        count = listening_count.count
        if track_id in track_listening_count_map:
            track_listening_count_map[track_id] += count
        else:
            track_listening_count_map[track_id] = count
    return track_listening_count_map


def get_top_n_tracks(max_items: int, track_listening_count_map: dict):
    def insert(item: Tuple[str, int], acc: list):
        if len(acc) == 0:
            return [item]

        _, count = item
        i = -1
        for _, count_from_acc in acc:
            i += 1
            if count_from_acc <= count:
                return acc[:i] + [item] + acc[i:max_items - i - 1]
        return acc

    def helper(acc: list, item: Tuple[str, int]):
        _, total_count = item
        if len(acc) < 100:
            return insert(item, acc)
        elif acc[99][1] < total_count:
            return insert(item, acc)
        return acc

    return reduce(helper, track_listening_count_map.items(), [])


def map_lines(file_object):
    first = True
    while True:
        if first:
            first = False
            file_object.readline()
            continue
        line = file_object.readline()
        if not line:
            break
        yield TrackListeningCount(line)


def find_track_info(track_id: str):
    with open('./lfm-b2/tracks.tsv', 'r') as handle:
        while True:
            line = handle.readline()
            if not line:
                break
            if line.startswith(track_id):
                track_id, artist_name, track_name = line.replace(
                    '\n', '').split('\t')
                return f'{artist_name} -- {track_name} [{track_id}]'


def print_tracks(track_count_list: list):
    for track_id, count in track_count_list:
        track_info = find_track_info(track_id)
        print(f'|{count}|\t' + track_info)


def main():
    track_listening_count_map = None
    with open('./lfm-b2/listening-counts.tsv', 'r') as handle:
        print('Opened listening-counts.tsv')
        track_listening_counts = map_lines(handle)
        track_listening_count_map = count_track_listenings(
            track_listening_counts)
        print('Counted track listenings')
    top_100_tracks = get_top_n_tracks(100, track_listening_count_map)
    top_100_tracks = [('36346257', 284021), ('32496162', 233427), ('33619193', 223400), ('32083560', 211291), ('45222862', 211148), ('26445594', 209858), ('12234625', 208016), ('7527795', 207539), ('36039983', 206156), ('20926153', 205593), ('43433165', 203468), ('24361147', 179913), ('37909221', 177466), ('9793081', 177047), ('7247506', 177018), ('27263282', 175791), ('10540381', 175059), ('9245495', 169124), ('10407347', 168709), ('8336682', 168607), ('32376842', 167208), ('35837120', 165383), ('20562662', 163801), ('33762401', 162397), ('36367985', 162290), ('22268461', 160085), ('45362359', 158928), (
        '35019041', 157681), ('30412722', 156462), ('35051782', 155058), ('38944354', 152211), ('40525216', 150780), ('22461110', 150559), ('21117230', 150154), ('34986332', 149525), ('12327833', 148813), ('8325801', 146475), ('28979867', 144726), ('24933346', 144668), ('43590126', 144666), ('37090419', 143072), ('24551879', 141694), ('14901552', 139717), ('18526104', 139133), ('8944529', 138503), ('16466738', 138016), ('14233787', 135960), ('44793292', 135711), ('15250346', 134798), ('44219294', 134760), ('38045207', 134727), ('11520441', 134517), ('31469731', 133639), ('28859870', 133616), ('30439157', 133403)]
    print('Got top 100 tracks:')
    print_tracks(top_100_tracks)


if __name__ == '__main__':
    main()
