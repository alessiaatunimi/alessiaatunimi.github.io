import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from publications import parse, SOURCE


class BibliographyTests(unittest.TestCase):
    def test_source_has_all_entries_and_updated_metadata(self):
        entries = parse(SOURCE.read_text())
        self.assertEqual(len(entries), 18)
        indexed = {e['id']: e for e in entries}
        self.assertEqual(indexed['2434_1229975']['year'], 2026)
        self.assertIn('S. Lehmann', indexed['2434_1225897']['authors'])
        self.assertIn('F. Bäuerlein', indexed['2434_1225897']['authors'])
        self.assertEqual(sum(e['featured'] for e in entries), 3)
        self.assertEqual(sum(e['type'] == 'phdthesis' for e in entries), 1)
        self.assertEqual(indexed['2434_1225898']['link'], 'https://doi.org/10.1016/j.bcra.2025.100356')
        self.assertTrue(all(e['link'].startswith('https://') for e in entries))

    def test_new_entry_strings_accents_and_multiple_areas(self):
        text = r'''@string{venue = "A journal"}
        @article{new, title={A {Web3} study}, author={M{\"u}ller, A. and Doe, Jane},
          year=2027, journal=venue, areas={networks; learning}, featured={true},
          doi={https://doi.org/10.1234/example}}
        '''
        entry = parse(text)[0]
        self.assertEqual(entry['title'], 'A Web3 study')
        self.assertEqual(entry['authors'], 'A. Müller, Jane Doe')
        self.assertEqual(entry['venue'], 'A journal')
        self.assertEqual(entry['areas'], ['networks', 'learning'])
        self.assertTrue(entry['featured'])

    def test_duplicate_keys_fail(self):
        entry = '@article{a,title={Test},author={A},year={2025}}'
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            parse(entry + entry)

    def test_invalid_input_fails(self):
        cases = [
            '@article{a,title={Test},author={A},year={2025}',
            '@article{a,title={Test},year={2025}}',
            '@article{a,title={Test},author={A},year={2025},areas={typo}}',
            '@article{a,title={Test},author={A},year={2025},url={javascript:alert(1)}}',
            '@article{a,title={Test},author={A},year={tomorrow}}',
        ]
        for text in cases:
            with self.subTest(text=text), self.assertRaises(Exception):
                parse(text)

    def test_unclassified_entries_stay_in_all_and_order_is_newest_first(self):
        entries = parse('@misc{old,title={Old},author={A},year={2021}}\n'
                        '@misc{new,title={New},author={A},year={2026},areas={social}}')
        self.assertEqual([e['id'] for e in entries], ['new', 'old'])
        self.assertEqual(entries[1]['areas'], [])


if __name__ == '__main__':
    unittest.main()
