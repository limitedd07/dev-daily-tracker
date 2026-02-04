"""
Enhanced Learning Log Updater
Generates daily learning entries with idempotency, rich topic pools, and seeded randomization
"""

import random
import sys
from datetime import datetime
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

AI_TOPICS = [
    {
        "topic": "Transformer Architecture",
        "difficulty": "Advanced",
        "short": "Transformers use self-attention mechanisms to process sequences in parallel.",
        "deep": "The Transformer architecture revolutionized NLP by replacing recurrence with self-attention, enabling parallel processing and better long-range dependencies through multi-head attention and positional encoding.",
        "link": "https://arxiv.org/abs/1706.03762"
    },
    {
        "topic": "BERT Pre-training",
        "difficulty": "Advanced",
        "short": "BERT uses masked language modeling and next sentence prediction for pre-training.",
        "deep": "BERT (Bidirectional Encoder Representations from Transformers) pre-trains on unlabeled text using MLM and NSP tasks, creating contextual embeddings that transfer well to downstream tasks.",
        "link": "https://arxiv.org/abs/1810.04805"
    },
    {
        "topic": "Retrieval-Augmented Generation (RAG)",
        "difficulty": "Intermediate",
        "short": "RAG improves LLM accuracy by retrieving documents before generation.",
        "deep": "RAG combines retrieval systems with language models to ground responses in external knowledge, reducing hallucinations and improving factual accuracy through document-augmented generation.",
        "link": "https://www.pinecone.io/learn/retrieval-augmented-generation/"
    },
    {
        "topic": "Diffusion Models",
        "difficulty": "Advanced",
        "short": "Diffusion models generate images by iteratively denoising random noise.",
        "deep": "Diffusion models learn to reverse a gradual noising process, generating high-quality images through learned denoising steps. They power tools like DALL-E 2 and Stable Diffusion.",
        "link": "https://arxiv.org/abs/2006.11239"
    },
    {
        "topic": "Reinforcement Learning Basics",
        "difficulty": "Intermediate",
        "short": "RL trains agents through trial and error using rewards and penalties.",
        "deep": "Reinforcement Learning uses Markov Decision Processes where agents learn optimal policies by maximizing cumulative rewards through exploration and exploitation balancing.",
        "link": "https://spinningup.openai.com/en/latest/"
    },
    {
        "topic": "GANs (Generative Adversarial Networks)",
        "difficulty": "Advanced",
        "short": "GANs use two competing networks to generate realistic synthetic data.",
        "deep": "GANs pit a generator against a discriminator in a minimax game, where the generator learns to create increasingly realistic samples that fool the discriminator.",
        "link": "https://arxiv.org/abs/1406.2661"
    },
    {
        "topic": "Vector Databases",
        "difficulty": "Intermediate",
        "short": "Vector databases store and query high-dimensional embeddings efficiently.",
        "deep": "Vector databases like Pinecone and Weaviate enable semantic search by storing embeddings and performing fast approximate nearest neighbor searches using indexes like HNSW.",
        "link": "https://www.pinecone.io/learn/vector-database/"
    },
    {
        "topic": "Fine-tuning vs Prompt Engineering",
        "difficulty": "Beginner",
        "short": "Fine-tuning adapts models through training; prompting guides through instructions.",
        "deep": "Fine-tuning updates model weights on task-specific data, while prompt engineering crafts input instructions to elicit desired behaviors without changing weights.",
        "link": "https://platform.openai.com/docs/guides/fine-tuning"
    },
    {
        "topic": "Attention Mechanisms",
        "difficulty": "Intermediate",
        "short": "Attention allows models to focus on relevant parts of input sequences.",
        "deep": "Attention mechanisms compute weighted combinations of inputs based on learned relevance scores, enabling models to dynamically focus on important context across long sequences.",
        "link": "https://arxiv.org/abs/1409.0473"
    },
    {
        "topic": "Transfer Learning in NLP",
        "difficulty": "Intermediate",
        "short": "Transfer learning reuses pre-trained models for new tasks with less data.",
        "deep": "Transfer learning leverages knowledge from large-scale pre-training (e.g., GPT, BERT) and fine-tunes on specific tasks, dramatically reducing data and compute requirements.",
        "link": "https://ruder.io/transfer-learning/"
    },
    {
        "topic": "Neural Architecture Search (NAS)",
        "difficulty": "Advanced",
        "short": "NAS automates the design of neural network architectures.",
        "deep": "NAS uses algorithms (evolutionary, RL-based, or gradient-based) to automatically discover optimal network architectures for specific tasks, often outperforming hand-designed models.",
        "link": "https://arxiv.org/abs/1611.01578"
    },
    {
        "topic": "Contrastive Learning",
        "difficulty": "Intermediate",
        "short": "Contrastive learning trains models by comparing similar and dissimilar samples.",
        "deep": "Contrastive learning methods like SimCLR learn representations by pulling similar samples closer and pushing dissimilar ones apart in embedding space, enabling effective self-supervised learning.",
        "link": "https://arxiv.org/abs/2002.05709"
    },
    {
        "topic": "Large Language Models (LLMs)",
        "difficulty": "Advanced",
        "short": "LLMs are massive models trained on vast text corpora for language understanding.",
        "deep": "LLMs like GPT-4 use billions of parameters trained on diverse text data, exhibiting emergent abilities like few-shot learning, reasoning, and instruction following.",
        "link": "https://openai.com/research/gpt-4"
    },
    {
        "topic": "Embedding Spaces",
        "difficulty": "Intermediate",
        "short": "Embeddings map discrete tokens to continuous vector representations.",
        "deep": "Embedding spaces represent words, sentences, or images as vectors where semantic similarity correlates with geometric proximity, enabling mathematical operations on meaning.",
        "link": "https://www.tensorflow.org/text/guide/word_embeddings"
    },
    {
        "topic": "Model Quantization",
        "difficulty": "Intermediate",
        "short": "Quantization reduces model size by using lower precision numbers.",
        "deep": "Quantization techniques convert 32-bit floats to 8-bit integers, dramatically reducing memory and compute requirements while maintaining acceptable accuracy for deployment.",
        "link": "https://pytorch.org/docs/stable/quantization.html"
    }
]

DSA_TOPICS = [
    {
        "topic": "Binary Search on Answer",
        "difficulty": "Intermediate",
        "short": "Binary Search on Answer applies binary search to the solution space.",
        "deep": "This technique binary searches over possible answers (not array indices) for optimization problems where feasibility is monotonic, like finding minimum capacity or maximum value.",
        "link": "https://leetcode.com/problems/koko-eating-bananas/"
    },
    {
        "topic": "Sliding Window Technique",
        "difficulty": "Intermediate",
        "short": "Sliding window maintains a subarray/substring while traversing sequences.",
        "deep": "The sliding window pattern uses two pointers to maintain a dynamic window, expanding and contracting to find optimal subarrays for problems like longest substring or maximum sum.",
        "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
    },
    {
        "topic": "Dynamic Programming Patterns",
        "difficulty": "Advanced",
        "short": "DP breaks problems into overlapping subproblems with optimal substructure.",
        "deep": "Dynamic Programming solves optimization problems by storing solutions to subproblems, using memoization (top-down) or tabulation (bottom-up) to avoid redundant computation.",
        "link": "https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns"
    },
    {
        "topic": "Graph Traversal (BFS/DFS)",
        "difficulty": "Intermediate",
        "short": "BFS explores level-by-level; DFS explores depth-first with backtracking.",
        "deep": "BFS uses queues for shortest path in unweighted graphs; DFS uses stacks/recursion for cycle detection, topological sorting, and connected components.",
        "link": "https://leetcode.com/problems/number-of-islands/"
    },
    {
        "topic": "Trie Data Structure",
        "difficulty": "Intermediate",
        "short": "Tries store strings in a tree for efficient prefix-based operations.",
        "deep": "Tries (prefix trees) enable O(L) insert/search for strings of length L, supporting autocomplete, spell-checking, and IP routing through character-based branching.",
        "link": "https://leetcode.com/problems/implement-trie-prefix-tree/"
    },
    {
        "topic": "Union-Find (Disjoint Set)",
        "difficulty": "Intermediate",
        "short": "Union-Find tracks connected components with near-constant time operations.",
        "deep": "Union-Find uses path compression and union by rank to achieve O(α(n)) amortized time for union/find operations, essential for Kruskal's MST and cycle detection.",
        "link": "https://leetcode.com/problems/redundant-connection/"
    },
    {
        "topic": "Two Pointers Technique",
        "difficulty": "Beginner",
        "short": "Two pointers traverse arrays/strings from different positions simultaneously.",
        "deep": "Two pointer patterns (opposite ends, same direction, or fast-slow) reduce time complexity from O(n²) to O(n) for problems like pair finding and palindrome checking.",
        "link": "https://leetcode.com/problems/container-with-most-water/"
    },
    {
        "topic": "Monotonic Stack/Queue",
        "difficulty": "Intermediate",
        "short": "Monotonic structures maintain sorted order while processing sequences.",
        "deep": "Monotonic stacks/queues keep elements in increasing/decreasing order, enabling O(n) solutions for next greater element, largest rectangle, and sliding window maximum.",
        "link": "https://leetcode.com/problems/next-greater-element-i/"
    },
    {
        "topic": "Backtracking",
        "difficulty": "Intermediate",
        "short": "Backtracking explores all possible solutions by building candidates incrementally.",
        "deep": "Backtracking builds solutions piece-by-piece, abandoning invalid paths (pruning) to solve constraint satisfaction problems like N-Queens, Sudoku, and permutations.",
        "link": "https://leetcode.com/problems/n-queens/"
    },
    {
        "topic": "Topological Sort",
        "difficulty": "Intermediate",
        "short": "Topological sort orders DAG vertices respecting all edge directions.",
        "deep": "Topological sorting uses DFS or Kahn's algorithm (BFS with in-degree) to linearize directed acyclic graphs, crucial for task scheduling and dependency resolution.",
        "link": "https://leetcode.com/problems/course-schedule-ii/"
    },
    {
        "topic": "Segment Trees",
        "difficulty": "Advanced",
        "short": "Segment trees enable efficient range queries and updates.",
        "deep": "Segment trees are binary trees where each node represents an interval, supporting O(log n) range sum/min/max queries and updates through lazy propagation.",
        "link": "https://leetcode.com/articles/a-recursive-approach-to-segment-trees-range-sum-queries-lazy-propagation/"
    },
    {
        "topic": "Binary Indexed Tree (Fenwick Tree)",
        "difficulty": "Advanced",
        "short": "BIT supports efficient prefix sum queries and updates.",
        "deep": "Fenwick Trees use clever bit manipulation to store partial sums, enabling O(log n) point updates and prefix sum queries in a space-efficient array structure.",
        "link": "https://leetcode.com/problems/range-sum-query-mutable/"
    },
    {
        "topic": "Dijkstra's Algorithm",
        "difficulty": "Advanced",
        "short": "Dijkstra finds shortest paths in weighted graphs with non-negative edges.",
        "deep": "Dijkstra's algorithm uses a priority queue to greedily select the nearest unvisited vertex, relaxing edges to find shortest paths from a source in O((V+E)log V).",
        "link": "https://leetcode.com/problems/network-delay-time/"
    },
    {
        "topic": "KMP String Matching",
        "difficulty": "Advanced",
        "short": "KMP finds pattern occurrences in O(n+m) using partial match table.",
        "deep": "Knuth-Morris-Pratt algorithm preprocesses the pattern to build an LPS (Longest Prefix Suffix) array, enabling linear time string matching without backtracking.",
        "link": "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/"
    },
    {
        "topic": "Bit Manipulation Tricks",
        "difficulty": "Intermediate",
        "short": "Bit manipulation uses bitwise operations for efficient computation.",
        "deep": "Techniques like XOR for finding unique elements, bit masking for subsets, and Brian Kernighan's algorithm for counting set bits enable O(1) or O(log n) operations.",
        "link": "https://leetcode.com/problems/single-number/"
    }
]

SYSTEM_DESIGN_TOPICS = [
    {
        "topic": "Load Balancing Strategies",
        "difficulty": "Intermediate",
        "short": "Load balancing distributes traffic across servers for scalability.",
        "deep": "Load balancers use algorithms (round-robin, least connections, consistent hashing) to distribute requests, improving availability and preventing server overload through health checks.",
        "link": "https://www.nginx.com/resources/glossary/load-balancing/"
    },
    {
        "topic": "Database Sharding",
        "difficulty": "Advanced",
        "short": "Sharding partitions databases horizontally across multiple servers.",
        "deep": "Sharding splits data by keys (hash, range, or geography) to scale beyond single-machine limits, requiring careful key selection to avoid hotspots and maintain query efficiency.",
        "link": "https://www.mongodb.com/features/database-sharding-explained"
    },
    {
        "topic": "CAP Theorem",
        "difficulty": "Advanced",
        "short": "CAP theorem states distributed systems can't guarantee all three: Consistency, Availability, Partition tolerance.",
        "deep": "CAP theorem proves distributed databases must choose two of three guarantees during network partitions: CP systems (MongoDB) sacrifice availability; AP systems (Cassandra) allow eventual consistency.",
        "link": "https://www.ibm.com/topics/cap-theorem"
    },
    {
        "topic": "Caching Strategies",
        "difficulty": "Intermediate",
        "short": "Caching stores frequently accessed data in fast storage layers.",
        "deep": "Cache strategies (write-through, write-back, write-around) and eviction policies (LRU, LFU, FIFO) optimize read latency and reduce database load using Redis or Memcached.",
        "link": "https://redis.io/docs/manual/patterns/caching/"
    },
    {
        "topic": "Message Queues",
        "difficulty": "Intermediate",
        "short": "Message queues decouple services through asynchronous communication.",
        "deep": "Message queues like RabbitMQ and Kafka buffer messages between producers and consumers, enabling async processing, load leveling, and fault tolerance through durable persistence.",
        "link": "https://aws.amazon.com/message-queue/"
    },
    {
        "topic": "Content Delivery Networks (CDN)",
        "difficulty": "Beginner",
        "short": "CDNs cache content at edge locations near users for faster delivery.",
        "deep": "CDNs like Cloudflare distribute static assets globally, reducing latency through geographic proximity, offloading origin servers, and providing DDoS protection.",
        "link": "https://www.cloudflare.com/learning/cdn/what-is-a-cdn/"
    },
    {
        "topic": "Microservices Architecture",
        "difficulty": "Advanced",
        "short": "Microservices decompose applications into independently deployable services.",
        "deep": "Microservices architecture enables scalability and team autonomy but introduces complexity in service discovery, distributed transactions, data consistency, and inter-service communication.",
        "link": "https://microservices.io/"
    },
    {
        "topic": "Rate Limiting",
        "difficulty": "Intermediate",
        "short": "Rate limiting controls request rates to prevent abuse and overload.",
        "deep": "Rate limiting algorithms (token bucket, leaky bucket, fixed/sliding window) protect APIs from abuse, using Redis for distributed counters and returning 429 status codes.",
        "link": "https://www.cloudflare.com/learning/bots/what-is-rate-limiting/"
    },
    {
        "topic": "Database Indexing",
        "difficulty": "Intermediate",
        "short": "Indexes accelerate database queries by creating searchable data structures.",
        "deep": "B-tree and hash indexes trade write performance for read speed, requiring careful selection based on query patterns to avoid index bloat and maintain optimal query plans.",
        "link": "https://use-the-index-luke.com/"
    },
    {
        "topic": "Consistent Hashing",
        "difficulty": "Advanced",
        "short": "Consistent hashing minimizes key redistribution when nodes change.",
        "deep": "Consistent hashing maps keys and nodes to a ring, ensuring only K/n keys move when nodes join/leave (vs K keys in naive hashing), critical for distributed caches and databases.",
        "link": "https://www.toptal.com/big-data/consistent-hashing"
    },
    {
        "topic": "Event-Driven Architecture",
        "difficulty": "Advanced",
        "short": "Event-driven systems communicate through asynchronous event notifications.",
        "deep": "Event-driven architectures use event buses and message brokers for loose coupling, enabling reactive systems, CQRS patterns, and event sourcing for audit trails.",
        "link": "https://aws.amazon.com/event-driven-architecture/"
    },
    {
        "topic": "API Gateway Pattern",
        "difficulty": "Intermediate",
        "short": "API gateways provide a single entry point for client requests.",
        "deep": "API gateways handle authentication, rate limiting, request routing, and protocol translation, abstracting backend complexity while providing monitoring and analytics.",
        "link": "https://microservices.io/patterns/apigateway.html"
    },
    {
        "topic": "Database Replication",
        "difficulty": "Intermediate",
        "short": "Replication copies data across multiple database instances for availability.",
        "deep": "Master-slave replication scales reads and provides failover, while multi-master enables writes at multiple nodes with conflict resolution strategies for eventual consistency.",
        "link": "https://www.postgresql.org/docs/current/high-availability.html"
    },
    {
        "topic": "Circuit Breaker Pattern",
        "difficulty": "Advanced",
        "short": "Circuit breakers prevent cascading failures by stopping calls to failing services.",
        "deep": "Circuit breakers monitor failure rates, opening to fail fast and closing after recovery periods, preventing resource exhaustion during downstream service failures.",
        "link": "https://martinfowler.com/bliki/CircuitBreaker.html"
    },
    {
        "topic": "Horizontal vs Vertical Scaling",
        "difficulty": "Beginner",
        "short": "Vertical scaling adds resources to one machine; horizontal scaling adds more machines.",
        "deep": "Horizontal scaling (scale-out) adds commodity servers for better fault tolerance and unlimited growth, while vertical scaling (scale-up) has hardware limits but simpler architecture.",
        "link": "https://www.section.io/blog/scaling-horizontally-vs-vertically/"
    }
]

# ============================================
# MAIN LOGIC
# ============================================

def main():
    """Main entry point for learning log updates"""
    
    # Get current date and setup
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    day_name = today.strftime("%A")
    is_weekend = day_name in ["Saturday", "Sunday"]
    
    print(f"🔄 Running learning update for {date_str} ({day_name})")
    
    # Setup paths
    learning_log = Path("learning_log.md")
    activity_log = Path("activity_log.md")
    linkedin_post = Path("linkedin_post.md")
    linkedin_prompt = Path("linkedin_image_prompt.txt")
    
    # ============================================
    # IDEMPOTENCY CHECK
    # ============================================
    
    if learning_log.exists():
        content = learning_log.read_text(encoding="utf-8")
        if f"## {date_str}" in content:
            print(f"✅ Entry for {date_str} already exists, skipping to prevent duplicates")
            sys.exit(0)
    
    # ============================================
    # SEEDED RANDOMIZATION
    # ============================================
    
    # Use date as seed for reproducibility (same day = same topic)
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    
    # Select domain and topic
    domains = {
        "AI": AI_TOPICS,
        "DSA": DSA_TOPICS,
        "System Design": SYSTEM_DESIGN_TOPICS
    }
    
    domain = random.choice(list(domains.keys()))
    selected = random.choice(domains[domain])
    
    # Choose explanation length based on day
    explanation = selected["deep"] if is_weekend else selected["short"]
    
    print(f"📚 Selected topic: [{domain}] {selected['topic']}")
    print(f"   Difficulty: {selected['difficulty']}")
    
    # ============================================
    # UPDATE LEARNING LOG
    # ============================================
    
    try:
        # Initialize file if it doesn't exist
        if not learning_log.exists():
            learning_log.write_text("# 📚 Daily Learning Log\n\n", encoding="utf-8")
        
        # Append new entry
        entry = f"\n## {date_str} — [{domain}] {selected['topic']}\n"
        entry += f"**Difficulty:** {selected['difficulty']}\n\n"
        entry += f"{explanation}\n\n"
        entry += f"🔗 Reference: {selected['link']}\n"
        
        with learning_log.open("a", encoding="utf-8") as f:
            f.write(entry)
        
        print(f"✅ Updated {learning_log}")
        
    except Exception as e:
        print(f"❌ Error updating learning log: {e}")
        sys.exit(1)
    
    # ============================================
    # CREATE LINKEDIN POST
    # ============================================
    
    try:
        post_content = f"""🚀 Daily Learning Update

Today I explored **{selected['topic']}** ({domain}).

{explanation}

#LearningInPublic #AI #DSA #SystemDesign #SoftwareEngineering"""
        
        linkedin_post.write_text(post_content, encoding="utf-8")
        print(f"✅ Created {linkedin_post}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create LinkedIn post: {e}")
    
    # ============================================
    # CREATE IMAGE PROMPT
    # ============================================
    
    try:
        prompt_content = f"""Create a clean LinkedIn post image.
Topic: {selected['topic']}
Domain: {domain}
Style: Minimal, professional, flat illustration."""
        
        linkedin_prompt.write_text(prompt_content, encoding="utf-8")
        print(f"✅ Created {linkedin_prompt}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create image prompt: {e}")
    
    # ============================================
    # WEEKLY SUMMARY PLACEHOLDER
    # ============================================
    
    if day_name == "Sunday":
        try:
            weekly_summary = Path("weekly_summary.md")
            
            # Initialize if needed
            if not weekly_summary.exists():
                weekly_summary.write_text("# 📊 Weekly Learning Summaries\n\n", encoding="utf-8")
            
            # Add placeholder for manual weekly review
            with weekly_summary.open("a", encoding="utf-8") as f:
                f.write(f"\n## Week of {date_str}\n")
                f.write("- [ ] Review learning log for this week\n")
                f.write("- [ ] Identify key takeaways\n")
                f.write("- [ ] Plan next week's focus\n")
            
            print(f"✅ Added weekly summary placeholder")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not update weekly summary: {e}")
    
    print(f"\n🎉 Learning update completed successfully!")

if __name__ == "__main__":
    main()
