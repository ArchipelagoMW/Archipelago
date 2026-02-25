import json

if __name__ == "__main__":
    from worlds.candybox2.rules import CandyBox2RulesPackage, generate_rules_package

    rules_package = generate_rules_package()
    rules_package_json = json.dumps(rules_package, cls=CandyBox2RulesPackage, indent=2)
    print(rules_package_json)

    with open("candy_box_2_rules.json", "w") as f:
        f.write(rules_package_json)
