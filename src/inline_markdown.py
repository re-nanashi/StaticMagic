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
        matches = extract_markdown_images(old_node.text)
        split_nodes = []
        for image_tup in matches:
            sections = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if sections.count("") == len(sections):
                split_nodes.append(
                    TextNode(matches[0][0], TextType.text_type_image, matches[0][1]))
                continue
            i = 1 if sections[0] == "" else 0
            split_nodes.extend([TextNode(sections[i], TextType.text_type_text), TextNode(
                image_tup[0], TextType.text_type_image,  image_tup[1])])
            text = sections[i + 1]
            if len(extract_markdown_images(text)) == 0 and text != "":
                split_nodes.append(TextNode(text, TextType.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        split_nodes = []
        for link_tup in matches:
            sections = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if sections.count("") == len(sections):
                split_nodes.append(
                    TextNode(matches[0][0], TextType.text_type_link, matches[0][1]))
                continue
            i = 1 if sections[0] == "" else 0
            split_nodes.extend([TextNode(sections[i], TextType.text_type_text), TextNode(
                link_tup[0], TextType.text_type_link,  link_tup[1])])
            text = sections[i + 1]
            if len(extract_markdown_links(text)) == 0 and text != "":
                split_nodes.append(TextNode(text, TextType.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes
