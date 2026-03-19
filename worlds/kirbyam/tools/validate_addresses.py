"""
Validate addresses.json against client usage and document address correctness.

This script:
1. Loads addresses from worlds/kirbyam/data/addresses.json
2. Checks that each address is used in client.py
3. Validates address ranges don't overlap
4. Generates a usage report

Usage:
    python validate_addresses.py
    python validate_addresses.py --verbose
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple, List, Optional


class AddressValidator:
    """Validates address definitions and usage."""
    
    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize validator with paths."""
        if repo_root is None:
            # worlds/kirbyam/tools/validate_addresses.py -> go up 3 levels to kirbyam
            repo_root = Path(__file__).parent.parent
        
        self.repo_root = repo_root
        self.addresses_file = repo_root / "data" / "addresses.json"
        self.client_file = repo_root / "client.py"
        self.addresses: Dict[str, Dict[str, str]] = {}
        self.grouped_ram_sections: Dict[str, Dict[str, str]] = {}
        self.client_code: str = ""
        
    def load_addresses(self) -> bool:
        """Load addresses.json."""
        try:
            with open(self.addresses_file) as f:
                data = json.load(f)
                self.addresses = data
                ram = self.addresses.get("ram", {}) if isinstance(self.addresses, dict) else {}
                if isinstance(ram, dict):
                    transport = ram.get("transport")
                    native = ram.get("native")
                    if isinstance(transport, dict) or isinstance(native, dict):
                        self.grouped_ram_sections = {
                            "ram.transport": transport if isinstance(transport, dict) else {},
                            "ram.native": native if isinstance(native, dict) else {},
                        }
                    else:
                        self.grouped_ram_sections = {"ram": ram}

                total = 0
                for section in self.grouped_ram_sections.values():
                    total += len(section)
                rom = self.addresses.get("rom", {}) if isinstance(self.addresses, dict) else {}
                if isinstance(rom, dict):
                    total += len(rom)

                print(f"✓ Loaded {total} addresses")
                return True
        except Exception as e:
            print(f"✗ Failed to load addresses: {e}")
            return False
    
    def load_client_code(self) -> bool:
        """Load client.py source."""
        try:
            with open(self.client_file) as f:
                self.client_code = f.read()
                print(f"✓ Loaded client.py ({len(self.client_code)} bytes)")
                return True
        except Exception as e:
            print(f"✗ Failed to load client.py: {e}")
            return False
    
    def validate_usage(self) -> List[str]:
        """Check that addresses are used in client code."""
        issues = []
        informational_unused = {
            "debug_item_counter",
            "debug_last_item_id",
            "debug_last_from",
        }
        
        print("\n--- Address Usage Validation ---")
        
        sections: Dict[str, Dict[str, str]] = {}
        sections.update(self.grouped_ram_sections)
        rom = self.addresses.get("rom", {}) if isinstance(self.addresses, dict) else {}
        if isinstance(rom, dict):
            sections["rom"] = rom

        for section, addrs in sections.items():
            print(f"\n{section}:")
            for name, addr in addrs.items():
                # Search for address key usage in client
                if f'"{name}"' in self.client_code or f"'{name}'" in self.client_code:
                    print(f"  ✓ {name:30s} = {addr}")
                else:
                    if section == "ram.native" or name in informational_unused:
                        print(f"  • {name:30s} = {addr} (unused by current client path)")
                    else:
                        issue = f"Address '{name}' ({section}) not used in client.py"
                        issues.append(issue)
                        print(f"  ⚠ {name:30s} = {addr} (NOT USED)")
        
        return issues
    
    def validate_ranges(self) -> List[str]:
        """Check that address ranges don't overlap."""
        issues = []
        
        print("\n--- Address Range Validation ---")
        
        # Extract numeric values and check for overlap
        ranges: List[Tuple[str, int, int]] = []
        
        sections: Dict[str, Dict[str, str]] = {}
        sections.update(self.grouped_ram_sections)
        rom = self.addresses.get("rom", {}) if isinstance(self.addresses, dict) else {}
        if isinstance(rom, dict):
            sections["rom"] = rom

        for section, addrs in sections.items():
            for name, addr_str in addrs.items():
                try:
                    addr = int(addr_str, 16)
                    # Assume each entry is 4 bytes unless we know better
                    size = 4
                    ranges.append((name, addr, addr + size))
                except ValueError:
                    issues.append(f"Invalid address format: {name} = {addr_str}")
        
        # Check overlaps
        ranges.sort(key=lambda x: x[1])
        for i, (name1, start1, end1) in enumerate(ranges):
            for name2, start2, end2 in ranges[i+1:]:
                if start1 < start2 < end1 or start2 < start1 < end2:
                    overlap_addr = max(start1, start2)
                    issue = f"Overlap: {name1} (${start1:08X}-${end1:08X}) overlaps {name2} (${start2:08X}-${end2:08X}) at ${overlap_addr:08X}"
                    issues.append(issue)
                    print(f"  ⚠ {issue}")
        
        if not issues:
            print("  ✓ No overlapping ranges detected")
        
        return issues
    
    def print_summary(self, all_issues: List[str]) -> int:
        """Print validation summary."""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        if not all_issues:
            print("✓ All validations passed!")
            return 0
        else:
            print(f"✗ Found {len(all_issues)} issues:\n")
            for i, issue in enumerate(all_issues, 1):
                print(f"  {i}. {issue}")
            return 1
    
    def run(self) -> int:
        """Execute all validations."""
        print("Kirby AM Address Validator")
        print("="*70)
        
        if not self.load_addresses():
            return 1
        
        if not self.load_client_code():
            return 1
        
        all_issues = []
        all_issues.extend(self.validate_usage())
        all_issues.extend(self.validate_ranges())
        
        return self.print_summary(all_issues)


if __name__ == "__main__":
    validator = AddressValidator()
    sys.exit(validator.run())
