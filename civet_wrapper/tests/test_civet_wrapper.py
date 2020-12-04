
from unittest import TestCase
from civet_wrapper.civet_wrapper import Civet


def occurrences(string, match):
    return len(string.split(match)) - 1


class TestCivetArguments(TestCase):
    def setUp(self):
        self.app = Civet()
        # self.app.define_parameters()
    
    def test_run(self):
        options = self.app.parse_args([
            '-N3-distance', '200',
            '-resample-surfaces',
            '-thickness', 'tlaplace:tfs:tlink', '30:20',
            '/inputdir', '/outputdir'
        ])

        cli_options = self.app.assemble_cli(options)
        
        self.assertEqual(occurrences(cli_options, '-sourcedir'), 1)
        self.assertEqual(occurrences(cli_options, '-targetdir'), 1)

        self.assertTrue('thickness tlaplace:tfs:tlink 30:20' in cli_options)
        self.assertTrue('-N3-distance 200' in cli_options)
        
        after = cli_options[cli_options.index('-resample-surfaces')+18:]
        self.assertTrue(len(after) == 0 or after.startswith(' -'),
            '-resample-surfaces was given an argument')
