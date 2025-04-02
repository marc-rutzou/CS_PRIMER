package algos.linear_structures.doubly;

public class Doubly {
    public static void main(String[] args) {
        Deque d = new Deque();
        assert d.size() == 0;
        int val = 4;
        d.push(val);
        assert d.pop() == val;
        assert d.size() == 0;

        System.out.printf("%nok%n");
    }
}

class Deque {
    private DoublyLinkedList dll;
    
    public Deque() {
        dll = new DoublyLinkedList();    
    }

    public void push(int e) { dll.addFirst(e); }

    public int pop() { 
        int ans = dll.first();
        dll.removeFirst();
        return ans;
    }

    public int size() { return dll.size(); }

    public void removeOld() { dll.removeLast(); }
}

class DoublyLinkedList {
    private Node head = null;
    private Node tail = null;
    private int size = 0;

    public DoublyLinkedList() {}

    public int size() { return this.size; }
    public boolean isEmpty() { return (this.size == 0); }

    public void addFirst(int element) {
        Node n = new Node(element, this.head, null);
        if (this.head != null) {
            this.head.setPrev(n);
        } else {
            this.tail = n;
        }
        this.head = n;
        this.size++;
    }

    public void addLast(int element) {
        Node n = new Node(element, null, this.tail);
        if (this.tail != null) {
            this.tail.setNext(n);
        } else {
            this.head = n;
        }
        this.tail = n;
        this.size++;
    }
    
    public void removeFirst() {
        if (this.isEmpty()) { 
            throw new IllegalStateException("DLL is empty");
        } else {
            this.head = this.head.getNext();
            this.size--;
        }
    }

    public void removeLast() {
        if (this.isEmpty()) { 
            throw new IllegalStateException("DLL is empty");
        } else {
            this.tail = this.tail.getPrev();        
            this.size--;
        }
    }

    public int first() {
        if (this.head != null) {
            return this.head.getElement();
        } else {
            throw new IllegalStateException("DLL is empty");
        }
    }

    public int last() {
        if (this.tail != null) {
            return this.tail.getElement();
        } else {
            throw new IllegalStateException("DLL is empty");
        }
    }

    public void removeElement(int element) {
        if (this.isEmpty()) { 
            System.out.printf("dll is empty%n");
        } else {
            Node n = this.head;
            while (n != null) {
                if (n.getElement() == element) {
                    if (n.getPrev() != null) { n.getPrev().setNext(n.getNext()); } else { this.head = n.getNext(); }
                    if (n.getNext() != null) { n.getNext().setPrev(n.getPrev()); } else { this.tail = n.getPrev(); }
                }   
                n = n.getNext();
            }
        }
    }

    public void print() {
        Node n = this.head;
        int counter = 1;
        while (n != null) {
            System.out.printf("%d: %d%n",counter, n.getElement());
            n = n.getNext();
        }
    }

    private class Node {
        private int element;
        private Node prev;
        private Node next;

        private Node (int element, Node next, Node prev) {
            this.element = element;
            this.next = next;
            this.prev = prev;
        }

        public Node getNext() { return this.next; }
        public Node getPrev() { return this.prev; }
        public int getElement() { return this.element; }

        public void setNext(Node n) { this.next = n; }
        public void setPrev(Node n) { this.prev = n; }
        public void setElement(int e) { this.element = e; }
    }
}
