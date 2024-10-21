import re

# Maven unused deps -> formatted into unused-deps.log
MAVEN_UNUSED_DEPS = 'mvn-deps.log'
UNUSED_DEPS = 'unused-deps.log'

# Jdeps output file -> formatted into used-deps.log
JDEPS_OUTPUT = 'jdeps-deps.log'
USED_DEPS = 'used-deps.log'

# Format mvn dependency lines to jar names
def format_unused_line(line):
    parts = line.strip().split(':')
    if len(parts) >= 4:
        group, artifact, _, version = parts[:4]
        return f"{artifact}-{version}.jar"
    return None

# Write formatted dependencies to a file
def format_unused_deps(input_file = MAVEN_UNUSED_DEPS, output_file = UNUSED_DEPS):

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            formatted_dep = format_unused_line(line)
            if formatted_dep:
                outfile.write(formatted_dep + '\n')
    print(f"\033[1mFormatted unused dependencies written to {output_file}...\033[0m")

# Parse jdeps output and write unique jar names to a file
def format_used_deps(input_file = JDEPS_OUTPUT, output_file = USED_DEPS):
    jar_pattern = re.compile(r'(\S+\.jar)')

    jars = set()

    with open(input_file, 'r') as file:
        for line in file:
            match = jar_pattern.search(line)
            if match:
                jars.add(match.group(1))

    with open(output_file, 'w') as file:
        for jar in sorted(jars):
            file.write(f"{jar}\n")

    print(f"\033[1mFormatterd used dependencies written to {output_file}...\033[0m")

def read_jars_from_file(file_path):
    """Read jar names from a specified file and return as a set."""
    with open(file_path, 'r') as file:
        return {line.strip() for line in file if line.strip()}

def compare_dep_lists(jars_file_1 = UNUSED_DEPS, jars_file_2 = USED_DEPS):
    """Compare jar names from two files and print differences."""
    jars_1 = read_jars_from_file(jars_file_1)
    jars_2 = read_jars_from_file(jars_file_2)

    missing_in_file_2 = jars_1 - jars_2
    missing_in_file_1 = jars_2 - jars_1
    shared_deps = jars_1 & jars_2

    # Print results
    if missing_in_file_2:
        print("\n\033[1m\033[91mUnused dependencies:\033[0m")
        for jar in sorted(missing_in_file_2):
            print(jar)
    else:
        print("No unused dependencies found.")
    
    if missing_in_file_1:
        print("\033[1m\033[92m\nUsed dependencies:\033[0m")
        for jar in sorted(missing_in_file_1):
            print(jar)
    else:
        print("No used dependencies found (???). This should not happen.")

    if shared_deps:
        print("\033[1m\033[93m\nShared dependencies:\033[0m")
        for jar in sorted(shared_deps):
            print(jar)
    else:
        print("\033[1m\033[93m\nNo shared dependencies found.\033[0m")



def main():
    format_unused_deps()
    format_used_deps()
    compare_dep_lists()

if __name__ == '__main__':
    main()