package introsort

import "math"

func IntroSort(lista []int) {
	var introsort func(int, int, int)

	introsort = func(inicio, fim, depth int) {
		size := fim - inicio + 1

		// insertion
		if size < 16 {
			for i := inicio + 1; i <= fim; i++ {
				key := lista[i]
				j := i - 1
				for j >= inicio && lista[j] > key {
					lista[j+1] = lista[j]
					j--
				}
				lista[j+1] = key
			}
			return
		}

		// heap sort
		if depth == 0 {
			heapSort(lista, inicio, fim)
			return
		}

		// quicksort
		p := partition(lista, inicio, fim)
		introsort(inicio, p-1, depth-1)
		introsort(p+1, fim, depth-1)
	}

	depth := int(2 * math.Log(float64(len(lista))))
	introsort(0, len(lista)-1, depth)
}

func partition(a []int, l, r int) int {
	pivot := a[r]
	i := l - 1
	for j := l; j < r; j++ {
		if a[j] <= pivot {
			i++
			a[i], a[j] = a[j], a[i]
		}
	}
	a[i+1], a[r] = a[r], a[i+1]
	return i + 1
}

func heapSort(a []int, l, r int) {
	n := r - l + 1

	for i := n/2 - 1; i >= 0; i-- {
		heapify(a, n, i, l)
	}

	for i := n - 1; i > 0; i-- {
		a[l], a[l+i] = a[l+i], a[l]
		heapify(a, i, 0, l)
	}
}

func heapify(a []int, n, i, off int) {
	maior := i
	esq := 2*i + 1
	dir := 2*i + 2

	if esq < n && a[off+esq] > a[off+maior] {
		maior = esq
	}
	if dir < n && a[off+dir] > a[off+maior] {
		maior = dir
	}

	if maior != i {
		a[off+i], a[off+maior] = a[off+maior], a[off+i]
		heapify(a, n, maior, off)
	}
}

//func main() {
//lista := []int{42, 7, 19, 3, 88, 15, 60, 1, 34, 27}
//fmt.Println("Antes:", lista)
//IntroSort(lista)
//fmt.Println("Depois:", lista)
//}
