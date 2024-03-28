from textnode import (TextNode, TextType)
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res_new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text_type_text:
            res_new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(
                    TextNode(sections[i], TextType.text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        res_new_nodes.extend(split_nodes)
    return res_new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text_type_text:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image_tup in images:
            sections = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if len(sections) != 2:
                raise ValueError(
                    "Invalid mardown syntax: Image section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.text_type_text))
            new_nodes.append(
                TextNode(image_tup[0], TextType.text_type_image, image_tup[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text_type_text:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link_tup in links:
            sections = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if len(sections) != 2:
                raise ValueError(
                    "Invalid mardown syntax: links section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.text_type_text))
            new_nodes.append(
                TextNode(link_tup[0], TextType.text_type_link, link_tup[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.text_type_text))
    return new_nodes


def text_to_textnode(text):
    node = TextNode(text, TextType.text_type_text)

    bold = split_nodes_delimiter([node], "**", TextType.text_type_bold)
    italic = split_nodes_delimiter(bold, "*", TextType.text_type_italic)
    code = split_nodes_delimiter(italic, "`", TextType.text_type_code)
    images = split_nodes_image(code)
    links = split_nodes_link(images)

    return links
