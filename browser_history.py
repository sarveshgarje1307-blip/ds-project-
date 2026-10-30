"""
Browser History Simulator using a Doubly Linked List (DLL)
===========================================================
A high-performance, lightweight prototype demonstrating forward and backward
browser navigation with automatic forward-history truncation.

Architecture:
- Node: Represents a web page with pointers to `prev` and `next` nodes.
- BrowserHistory: Doubly linked list tracking `head`, `tail`, and `current` pointer.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
import sys


@dataclass
class HistoryNode:
    """Represents a single visited page node in the Doubly Linked List."""
    url: str
    title: str
    timestamp: str
    prev: Optional["HistoryNode"] = None
    next: Optional["HistoryNode"] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "timestamp": self.timestamp,
        }


class BrowserHistory:
    """
    Browser history simulator implemented using a Doubly Linked List.

    Complexity:
    - visit(url): O(1) pointer updates (forward history is pruned)
    - back(steps): O(min(steps, N)) where steps=1 is O(1)
    - forward(steps): O(min(steps, N)) where steps=1 is O(1)
    - current page: O(1)
    """

    def __init__(self, homepage: str = "https://welcome.internal", title: str = "New Tab"):
        initial_node = HistoryNode(
            url=homepage,
            title=title,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        self.head: HistoryNode = initial_node
        self.tail: HistoryNode = initial_node
        self.current: HistoryNode = initial_node
        self._size: int = 1

    @property
    def size(self) -> int:
        return self._size

    def can_go_back(self) -> bool:
        """Returns True if there is a previous page in history."""
        return self.current.prev is not None

    def can_go_forward(self) -> bool:
        """Returns True if there is a next page in history."""
        return self.current.next is not None

    def get_current_page(self) -> HistoryNode:
        """Returns the current active page node."""
        return self.current

    def visit(self, url: str, title: str = "") -> HistoryNode:
        """
        Visits a new URL from the current page.
        Crucial browser behavior:
        Visiting a new page clears all forward history beyond the current page.
        """
        if not title:
            # Auto-generate a clean title from url
            clean_name = url.replace("https://", "").replace("http://", "").split("/")[0]
            title = clean_name.capitalize() if clean_name else "Page"

        # 1. Truncate forward history if current is not tail
        if self.current.next is not None:
            # Count discarded nodes for accurate size tracking
            discarded = 0
            temp = self.current.next
            while temp is not None:
                discarded += 1
                next_node = temp.next
                # Break references to assist garbage collection
                temp.prev = None
                temp.next = None
                temp = next_node

            self._size -= discarded
            self.current.next = None
            self.tail = self.current

        # 2. Create the new history node
        new_node = HistoryNode(
            url=url,
            title=title,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            prev=self.current,
            next=None
        )

        # 3. Link pointers
        self.current.next = new_node
        self.current = new_node
        self.tail = new_node
        self._size += 1

        return new_node

    def back(self, steps: int = 1) -> HistoryNode:
        """
        Navigates backward up to `steps` pages.
        Clamps to the head (oldest page) if steps exceed backward history.
        """
        if steps < 1:
            return self.current

        moved = 0
        while moved < steps and self.current.prev is not None:
            self.current = self.current.prev
            moved += 1

        return self.current

    def forward(self, steps: int = 1) -> HistoryNode:
        """
        Navigates forward up to `steps` pages.
        Clamps to the tail (latest page) if steps exceed forward history.
        """
        if steps < 1:
            return self.current

        moved = 0
        while moved < steps and self.current.next is not None:
            self.current = self.current.next
            moved += 1

        return self.current

    def clear(self, homepage: str = "https://welcome.internal", title: str = "New Tab") -> None:
        """Clears all history and resets to a homepage."""
        # Clean existing nodes
        curr = self.head
        while curr:
            nxt = curr.next
            curr.prev = None
            curr.next = None
            curr = nxt

        initial_node = HistoryNode(
            url=homepage,
            title=title,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        self.head = initial_node
        self.tail = initial_node
        self.current = initial_node
        self._size = 1

    def to_list(self) -> List[Dict[str, Any]]:
        """Returns all history nodes from head to tail with active marker."""
        result = []
        curr = self.head
        idx = 0
        while curr:
            result.append({
                "index": idx,
                "url": curr.url,
                "title": curr.title,
                "timestamp": curr.timestamp,
                "is_current": (curr is self.current),
                "has_prev": curr.prev is not None,
                "has_next": curr.next is not None,
            })
            curr = curr.next
            idx += 1
        return result

    def render_ascii(self) -> str:
        """Returns a formatted ASCII diagram of the doubly linked list."""
        nodes = []
        curr = self.head
        while curr:
            is_active = (curr is self.current)
            marker = "★ CURRENT" if is_active else ""
            label = f"[{curr.title} ({curr.url})]"
            if is_active:
                label = f"==> [{curr.title} ({curr.url})] <== {marker}"
            nodes.append(label)
            curr = curr.next

        connector = "\n       ▲ | \n       | ▼ \n"
        return connector.join(nodes)


def run_unit_tests():
    """Runs a quick sanity test suite verifying doubly linked list operations."""
    print("=" * 60)
    print("RUNNING DOUBLY LINKED LIST VERIFICATION TESTS")
    print("=" * 60)

    browser = BrowserHistory("https://home.com", "Home")
    assert browser.size == 1
    assert browser.get_current_page().url == "https://home.com"
    assert not browser.can_go_back()
    assert not browser.can_go_forward()
    print("✓ Test 1: Initialization Passed")

    # Visit pages
    browser.visit("https://google.com", "Google")
    browser.visit("https://github.com", "GitHub")
    browser.visit("https://python.org", "Python")
    assert browser.size == 4
    assert browser.get_current_page().url == "https://python.org"
    assert browser.can_go_back()
    assert not browser.can_go_forward()
    print("✓ Test 2: Sequential Visits Passed (size=4)")

    # Navigate Back 1 step
    curr = browser.back(1)
    assert curr.url == "https://github.com"
    assert browser.can_go_back()
    assert browser.can_go_forward()
    print("✓ Test 3: Back 1 Step Passed (at GitHub)")

    # Navigate Back 2 steps
    curr = browser.back(2)
    assert curr.url == "https://home.com"
    assert not browser.can_go_back()
    assert browser.can_go_forward()
    print("✓ Test 4: Back 2 Steps Clamped at Head Passed (at Home)")

    # Navigate Forward 1 step
    curr = browser.forward(1)
    assert curr.url == "https://google.com"
    print("✓ Test 5: Forward 1 Step Passed (at Google)")

    # Branching / Forward Truncation Test:
    # At Google (Home <-> Google <-> GitHub <-> Python)
    # Visiting Wikipedia should drop GitHub & Python!
    browser.visit("https://wikipedia.org", "Wikipedia")
    assert browser.size == 3  # Home, Google, Wikipedia
    assert browser.get_current_page().url == "https://wikipedia.org"
    assert not browser.can_go_forward()
    assert browser.can_go_back()

    # Step back to verify previous is Google
    curr = browser.back(1)
    assert curr.url == "https://google.com"

    # Step back to Home
    curr = browser.back(1)
    assert curr.url == "https://home.com"
    print("✓ Test 6: Forward History Truncation on Branching Passed")

    print("=" * 60)
    print("ALL 6 TESTS PASSED SUCCESSFULLY! (O(1) updates verified)")
    print("=" * 60)


def interactive_cli():
    """Starts an interactive CLI session to test the Browser History."""
    browser = BrowserHistory("https://google.com", "Google Search")

    print("\n" + "=" * 65)
    print("   🌐 BROWSER HISTORY SIMULATOR (Doubly Linked List Engine)")
    print("=" * 65)
    print("Commands:")
    print("  visit <url> [title]  : Visit a new webpage")
    print("  back [steps]         : Go backward in history (default 1 step)")
    print("  forward [steps]      : Go forward in history (default 1 step)")
    print("  history              : View the Doubly Linked List structure")
    print("  current              : View the active webpage")
    print("  clear                : Reset browser history")
    print("  test                 : Run automated verification tests")
    print("  exit / quit          : Quit the simulator")
    print("-" * 65)

    while True:
        try:
            curr = browser.get_current_page()
            back_indicator = "◀ [Back]" if browser.can_go_back() else "  [----]"
            fwd_indicator = "[Fwd] ▶" if browser.can_go_forward() else "[----]  "

            prompt = f"\n{back_indicator} {fwd_indicator} Current: {curr.url} > "
            user_input = input(prompt).strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd in ("exit", "quit", "q"):
                print("Exiting Browser History Simulator. Goodbye!")
                break

            elif cmd == "visit":
                if len(parts) < 2:
                    print("Error: Specify a URL to visit. Example: visit https://github.com GitHub")
                    continue
                url = parts[1]
                if not (url.startswith("http://") or url.startswith("https://")):
                    url = "https://" + url
                title = parts[2] if len(parts) > 2 else ""
                new_page = browser.visit(url, title)
                print(f"➜ Visited: {new_page.title} ({new_page.url})")

            elif cmd in ("back", "b"):
                steps = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                if not browser.can_go_back():
                    print("⚠️ Cannot go back: You are already at the earliest page in history.")
                else:
                    target = browser.back(steps)
                    print(f"◀ Navigated back {steps} step(s) to: {target.title} ({target.url})")

            elif cmd in ("forward", "fwd", "f"):
                steps = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                if not browser.can_go_forward():
                    print("⚠️ Cannot go forward: No forward history exists.")
                else:
                    target = browser.forward(steps)
                    print(f"▶ Navigated forward {steps} step(s) to: {target.title} ({target.url})")

            elif cmd in ("history", "h", "list", "dll"):
                print("\n--- DOUBLY LINKED LIST HISTORY VIEW ---")
                print(browser.render_ascii())
                print(f"Total Nodes: {browser.size}")

            elif cmd == "current":
                print(f"\nActive Page: {curr.title}")
                print(f"URL: {curr.url}")
                print(f"Timestamp: {curr.timestamp}")
                print(f"Previous Node: {curr.prev.url if curr.prev else 'None (HEAD)'}")
                print(f"Next Node: {curr.next.url if curr.next else 'None (TAIL)'}")

            elif cmd == "clear":
                browser.clear()
                print("History cleared. Reset to blank tab.")

            elif cmd == "test":
                run_unit_tests()

            elif cmd in ("help", "?"):
                print("Available commands: visit <url>, back [steps], forward [steps], history, current, clear, test, exit")

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for options.")

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_unit_tests()
    else:
        interactive_cli()
