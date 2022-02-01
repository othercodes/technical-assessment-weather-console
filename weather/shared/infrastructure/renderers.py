from typing import Dict, Optional

from weather.shared.domain.contracts import Renderer


class CLIRenderer(Renderer):
    def render(self, template: str, context: Optional[Dict[str, str]] = None):
        print(template.format(**context if context else {}))
