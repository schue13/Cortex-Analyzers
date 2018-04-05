#!/usr/bin/env python3
from cortexutils.analyzer import Analyzer
from stopforumspam_client import StopforumspamClient


class StopforumspamAnalyzer(Analyzer):
    """docstring for StopforumspamAnalyzer."""

    _malicious_default_confidence_level = 90.0
    _suspicious_default_confidence_level = 0.0

    def __init__(self):
        Analyzer.__init__(self)
        self.client = StopforumspamClient()
        self.malicious_confidence_level = self.get_param(
            'config.malicious_confidence_level',
            StopforumspamAnalyzer._malicious_default_confidence_level)
        self.suspicious_confidence_level = self.get_param(
            'config.suspicious_confidence_level',
            StopforumspamAnalyzer._suspicious_default_confidence_level)

    def summary(self, raw):
        taxonomies = []
        ns = 'SFS'
        predicate = self.data_type
        level = 'info'
        value = 0
        if 'results' in raw:
            if raw['results']:
                for r in raw['results']:
                    if r['appears']:
                        value = max(value, r['confidence'])
                if value > self.malicious_confidence_level:
                    level = 'malicious'
                elif value > self.suspicious_confidence_level:
                    level = 'suspicious'
                else:
                    level = 'safe'
        taxonomies.append(self.build_taxonomy(level, ns, predicate, value))
        return {'taxonomies': taxonomies}

    def run(self):
        if self.data_type == 'ip':
            self.report({
                'results': self.client.get_data(
                    self.data_type, self.get_data())
            })
        elif self.data_type == 'mail':
            self.report({
                'results': self.client.get_data(
                    self.data_type, self.get_data())
            })
        else:
            self.error('Unsupported dataType {}'.format(self.data_type))


if __name__ == '__main__':
    StopforumspamAnalyzer().run()
