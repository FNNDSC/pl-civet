
from unittest import TestCase
from unittest import mock
from civet_wrapper.civet_wrapper import Civet


def occurrences(string, match):
    return len(string.split(match)) - 1


class CivetTests(TestCase):
    """
    Test Civet.
    """
    def setUp(self):
        self.app = Civet()
    
    def test_run(self):
        """
        Test the run code.
        """
        args = []
        if self.app.TYPE == 'ds':
            args.append('inputdir') # you may want to change this inputdir mock
        args.append('outputdir')  # you may want to change this outputdir mock

        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)
        
        args.append('-N3-distance')
        args.append('200')
        args.append('-resample-surfaces')
        args.append('-thickness')
        args.append('tlaplace:tfs:tlink')
        args.append('30:20')

        options = self.app.parse_args(args)
        # self.app.run(options)
        cli_options = self.app.assemble_cli(options)
        # write your own assertions
        
        self.assertEqual(occurrences(cli_options, '-inputdir'), 1)
        self.assertEqual(occurrences(cli_options, '-outputdir'), 1)
        self.assertTrue('thickness tlaplace:tfs:tlink 30:20' in cli_options)
        self.assertTrue('-N3-distance 200' in cli_options)
        
        after = cli_options[cli_options.index('-resample-surfaces'):]
        self.assertTrue(len(after) == 0 or after.startswith(' -'))