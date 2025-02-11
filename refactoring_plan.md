# Brave Paladin Lean Refactoring Plan

## 1. Code Duplication Removal

### 1.1 Monster Behavior
Current issues:
- Duplicate animation state handling in skeleton_logic.py and zombie_logic.py
- Nearly identical setAnimation() methods
- Repeated state management code

Solution:
- Move common animation states to monster_behaviour.py
- Use composition over inheritance for unique monster traits
- Create simple factory for monster creation

### 1.2 Animation System
Current issues:
- Duplicate animation loading code
- Repeated animation state checks
- Similar sprite handling logic

Solution:
- Simplify animation state management
- Remove redundant checks
- Consolidate sprite loading logic

### 1.3 Resource Loading
Current issues:
- Similar JSON loading patterns in animation.py and map_data.py
- Duplicate error-prone file operations
- Redundant image loading checks

Solution:
- Create simple unified resource loading
- Remove redundant caching logic
- Simplify error handling

## 2. Unnecessary Abstraction Removal

### 2.1 Input System
Current issues:
- Over-engineered event system
- Commented out old input handling code
- Unnecessary indirection in key handling

Solution:
- Simplify to direct key mapping
- Remove unused input code
- Streamline event handling

### 2.2 Level System
Current issues:
- Complex inheritance chain
- Unused generator functionality
- Overly complex coordinate transformations

Solution:
- Flatten class hierarchy
- Remove unused level generation
- Simplify coordinate handling

### 2.3 Game Manager
Current issues:
- Mixed responsibilities
- Complex actor management
- Unnecessary state tracking

Solution:
- Separate core game logic
- Simplify actor lifecycle
- Remove redundant state management

## 3. Implementation Priority

### Phase 1: Remove Duplication
1. Consolidate monster behavior code
2. Unify animation handling
3. Simplify resource loading

### Phase 2: Simplify Systems
1. Streamline input handling
2. Clean up level system
3. Reorganize game manager

### Phase 3: Code Cleanup
1. Remove unused code
2. Fix inconsistent formatting
3. Improve error handling

## 4. Migration Strategy

1. Start with highest impact changes (monster/animation systems)
2. Make incremental improvements
3. Test functionality after each change
4. Remove deprecated code