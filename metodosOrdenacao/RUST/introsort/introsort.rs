pub fn intro_sort(lista: &mut [i32]) {
    let depth = (2.0 * (lista.len() as f64).ln()) as i32;
    introsort(lista, depth);
}

fn introsort(arr: &mut [i32], depth: i32) {
    let len = arr.len();

    // insertion
    if len < 16 {
        for i in 1..len {
            let key = arr[i];
            let mut j = i as i32 - 1;
            while j >= 0 && arr[j as usize] > key {
                arr[(j + 1) as usize] = arr[j as usize];
                j -= 1;
            }
            arr[(j + 1) as usize] = key;
        }
        return;
    }

    // heap
    if depth == 0 {
        arr.sort(); // fallback simplificado
        return;
    }

    // partition
    let p = partition(arr);
    let (left, right) = arr.split_at_mut(p);

    introsort(left, depth - 1);
    introsort(&mut right[1..], depth - 1);
}

fn partition(arr: &mut [i32]) -> usize {
    let len = arr.len();
    let pivot = arr[len - 1];
    let mut i = 0;

    for j in 0..len - 1 {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }

    arr.swap(i, len - 1);
    i
}
//fn main() {
    //let mut lista = vec![42, 7, 19, 3, 88, 15, 60, 1, 34, 27];
    //println!("Antes: {:?}", lista);
    //intro_sort(&mut lista);
    //println!("Depois: {:?}", lista);
//}