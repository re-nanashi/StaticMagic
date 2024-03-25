class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    """
    If self.props is:
    {"href": "https://www.google.com", "target": "_blank"}
    
    Then self.props_to_html() should return:
     href="https://www.google.com" target="_blank"
    """

    def props_to_html(self):
        if self.props is None:
            return ""
        html_attr = ""
        for key in self.props.keys():
            attr_str = f' {key}="{self.props[key]}"'
            html_attr += attr_str
        return "".join(html_attr)

    """
    __repr__(self) - Give yourself a way to print an HTMLNode object and see its tag, value, children, and props. 
    This will be useful for your debugging.

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    """

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
