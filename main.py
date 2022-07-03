from xml.etree import ElementTree
import csv
import argparse


class ScriptArguments:
    """ Helpful tool for adding arguments to the program before running it. """

    @property
    def input(self):
        """ Get input file name. """
        return self._input

    @property
    def output(self):
        """ Get output file name. """
        return self._output

    def __init__(self):
        self._parser = argparse.ArgumentParser(description="This is a XML to CVS data extractor (XML-parser).")
        self._parser.add_argument("input", help="Input file name (with XML extension).")
        self._parser.add_argument("output", help="Output file name (with CSV extension).")
        self._args = self._parser.parse_args()
        self._input = self._args.input
        self._output = self._args.output


class XMLParser:
    """ Class that will perform the XML parsing and extracting data to CSV file. """

    def __init__(self):
        self._scriptArgs = ScriptArguments()
        tree = ElementTree.parse(self._scriptArgs.input)
        root = tree.getroot()

        with open(self._scriptArgs.output, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            for conceptGrp in root.iter("conceptGrp"):
                concept = conceptGrp.find("concept").text

                # get terms.
                termDE = None
                termEN = None
                for languageGrp in conceptGrp.iter("languageGrp"):
                    language = languageGrp.find("language").attrib.get("type")
                    term = languageGrp.find("termGrp").find("term").text
                    if language == "de":
                        termDE = term
                    elif language == "en":
                        termEN = term
                writer.writerow([concept, termDE, termEN])


if __name__ == '__main__':
    xmlParser = XMLParser()
