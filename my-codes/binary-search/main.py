from bisect import bisect
def BinarySearch( nums: list, target):
    l = 0
    r = len(nums) -1


    while l < r:
        
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid + 1
        if nums[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    else:
        return False

if __name__ == "__main__":
    nums = [1, 2, 3, 5, 5, 6, 79, 90]
    target = 5
    print(bisect(nums, target))
    print(BinarySearch(nums, target))
