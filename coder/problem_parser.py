from bs4 import BeautifulSoup


class ProblemParser:
    @staticmethod
    def parse_leetcode_problem(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        def convert_formatting(element):
            formatting = {
                'sup': '^', 'sub': '_',
                'strong': '**', 'b': '**', 'em': '*', 'i': '*', 'code': '`'
            }
            if element.name in formatting:
                wrapper = formatting[element.name]
                return f"{wrapper}{convert_formatting_recursive(element)}{wrapper}"
            return element.string or convert_formatting_recursive(element)

        def convert_formatting_recursive(element):
            return ''.join(convert_formatting(child) for child in element.children)

        description = convert_formatting_recursive(soup.find('p'))
        conditions = [convert_formatting_recursive(li) for li in soup.find('ul').find_all('li')]
        examples = [f"Input: {example.find('strong', string='Input:').next_sibling.strip()}\n"
                    f"Output: {example.find('strong', string='Output:').next_sibling.strip()}"
                    for example in soup.find_all('pre')]
        constraints = [convert_formatting_recursive(li) for li in soup.find_all('ul')[-1].find_all('li')]

        return f"""Description:
    {description}

    Conditions:
    {chr(10).join('- ' + condition for condition in conditions)}

    Examples:
    {chr(10).join(examples)}

    Constraints:
    {chr(10).join('- ' + constraint for constraint in constraints)}
    """
