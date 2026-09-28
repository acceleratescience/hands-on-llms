from jinja2 import Environment, FileSystemLoader, Template


class TemplateManager:
    def __init__(self, template_dir: str = "prompts"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self._templates = {}
    
    def get_template(self, template_name: str, force_reload=False) -> Template:
        if template_name not in self._templates or force_reload:
            self._templates[template_name] = self.env.get_template(template_name)
        return self._templates[template_name]
    
    def render(self, template_name: str, force_reload=False, **kwargs) -> str:
        template = self.get_template(template_name, force_reload=force_reload)
        return template.render(**kwargs)