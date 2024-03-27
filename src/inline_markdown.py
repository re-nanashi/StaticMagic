from textnode import (TextNode, TextType)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res_new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            res_new_nodes.append(node)
            continue

        text = node.text
        new_nodes = []
        start = 0
        i = 0
        while i < len(text):
            if text[i:i+len(delimiter)] == delimiter:
                new_nodes.append(
                    TextNode(text[start: i], TextType.text_type_text))
                # Set start to the index of the starting char that is inside the delimiter
                i += len(delimiter)
                start = i
                # Loop until the ending char of the string inside delimiter is reached
                while i < len(text) and text[i:i+len(delimiter)] != delimiter:
                    i += 1
                # If matching closing delimiter not found, raise an exception
                if i == len(text):
                    raise Exception(
                        f"Invalid markdown sytanx: No matching closing delimiter found for delimiter at index: {start}")
                # Matching closing delimiter is found:
                new_nodes.append(TextNode(text[start: i], text_type))
                # Then, set the start after the closing delimiter
                i += len(delimiter)
                start = i
            else:
                i += 1
                # Lastly, if we reaced the end of the text and an exception wasn't raised, we have to add the last substring
                # of the original text and convert it into a textnode
                if i == len(text):
                    new_nodes.append(
                        TextNode(text[start: i], TextType.text_type_text))
        res_new_nodes.extend(new_nodes)
    return res_new_nodes
