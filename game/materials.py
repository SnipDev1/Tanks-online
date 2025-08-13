class Sprites:
    def __init__(self):
        self.texture_dictionary = self.set_image_paths()
        self.res_dictionary = None
        self.associate_id_with_names()
        # print(self.res_dictionary)

    def associate_id_with_names(self):
        self.res_dictionary = {}
        for key, value in self.texture_dictionary.items():
            if value['need_to_be_shown_in_editor']:
                self.res_dictionary[value["id"]] = key

    def set_image_paths(self):
        import json
        with open("materials.json", "r") as f:
            data = f.read()
        json_string = json.loads(data)
        return json_string

    def get_material_color_by_name(self, material_name):
        if material_name in self.texture_dictionary:
            return self.texture_dictionary[material_name]['color']
        else:
            return self.texture_dictionary["blank"]['color']

    def get_material_color_by_id(self, id):
        if id in self.res_dictionary:
            return self.texture_dictionary[self.res_dictionary[id]]['color']
        else:
            return self.texture_dictionary["blank"]['color']

    def get_image_path(self, material_name):
        if material_name in self.texture_dictionary:
            return self.texture_dictionary[material_name]['texture_path']
        else:
            return self.texture_dictionary["blank"]['texture_path']

    def get_material_data(self, material_name):
        if material_name in self.texture_dictionary:
            return self.texture_dictionary[material_name]
        else:
            return self.texture_dictionary["blank"]



if __name__ == '__main__':
    Sprites()
