import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnode
from textnode import text_node_to_html_node


class BlockType(Enum):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_unordered_list = "unordered_list"
    block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks


def block_to_block_type(markdown):
    def is_an_unordered_list_block(markdown):
        markdown_list = markdown.split("\n")
        ulist_sign = markdown_list[0][:2]
        if not (ulist_sign == "* " or ulist_sign == "- "):
            return False
        all_lines_starts_with_same_sign = all(
            line[:2] == ulist_sign for line in markdown_list)
        return all_lines_starts_with_same_sign

    def is_an_ordered_list_block(markdown):
        markdown_list = markdown.split("\n")
        flag = True
        current = 1
        for line in markdown_list:
            flag &= (line[0] == str(current) and line[1:3] == ". ")
            current += 1
        return flag

    if len(re.findall(r"^#{1,6}[^#]", markdown)) > 0:
        return BlockType.block_type_heading
    if markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockType.block_type_code
    if all(line[:2] == "> " for line in markdown.split("\n")):
        return BlockType.block_type_quote
    if is_an_unordered_list_block(markdown):
        return BlockType.block_type_unordered_list
    if is_an_ordered_list_block(markdown):
        return BlockType.block_type_ordered_list

    return BlockType.block_type_paragraph


def block_to_child_nodes(block):
    child_text_nodes = text_to_textnode(block)
    html_child_nodes = []
    for text_node in child_text_nodes:
        html_child_nodes.append(text_node_to_html_node(text_node))
    return html_child_nodes


def paragraph_block_to_html_node(paragraph_block):
    html_child_nodes = block_to_child_nodes(paragraph_block.replace("\n", " "))
    return ParentNode("p", html_child_nodes)


def heading_block_to_html_node(heading_block):
    count = heading_block[:7].count("#")
    if count > 6:
        raise ValueError(f"Invalid heading level: {count}")
    inline = heading_block.lstrip("# ")
    html_child_nodes = block_to_child_nodes(inline)
    return ParentNode(f"h{count}", html_child_nodes)


def ulist_block_to_html_node(ulist_block):
    block_items = ulist_block.split("\n")
    inline_items = [item[2:] for item in block_items]
    li_html_nodes = []
    for item in inline_items:
        li_html_nodes.append(
            (ParentNode("li", block_to_child_nodes(item))))
    return (ParentNode("ul", li_html_nodes))


def olist_block_to_html_node(olist_block):
    block_items = olist_block.split("\n")
    inline_items = [re.sub(r'^\d+\.\s*', '', item) for item in block_items]
    li_html_nodes = []
    for item in inline_items:
        li_html_nodes.append(
            (ParentNode("li", block_to_child_nodes(item))))
    return ParentNode("ol", li_html_nodes)


def quote_block_to_html_node_std(quote_block):
    inline_items = "\n".join([item.lstrip("> ")
                             for item in quote_block.split("\n")])
    parent_node = markdown_to_html_node(inline_items)
    parent_node.tag = "blockquote"
    return parent_node


def quote_block_to_html_node(quote_block):
    inline_items = " ".join([item.lstrip("> ")
                             for item in quote_block.split("\n")])
    html_child_nodes = block_to_child_nodes((inline_items))
    return ParentNode("blockquote", html_child_nodes)


def code_block_to_html_node(code_block):
    if not code_block.startswith("```") or not code_block.endswith("```"):
        raise ValueError("Invalid code block")
    inline_code = code_block[3:-3]
    html_child_nodes = block_to_child_nodes(inline_code)
    html_parent_node = ParentNode("code", html_child_nodes)
    return ParentNode("pre", [html_parent_node])


def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.block_type_quote:
                html_nodes.append(quote_block_to_html_node(block))
            case BlockType.block_type_unordered_list:
                html_nodes.append(ulist_block_to_html_node(block))
            case BlockType.block_type_ordered_list:
                html_nodes.append(olist_block_to_html_node(block))
            case BlockType.block_type_code:
                html_nodes.append(code_block_to_html_node(block))
            case BlockType.block_type_heading:
                html_nodes.append(heading_block_to_html_node(block))
            case BlockType.block_type_paragraph:
                html_nodes.append(paragraph_block_to_html_node(block))
            case _:
                raise ValueError("Invalid block type")
    return ParentNode("div", html_nodes)
