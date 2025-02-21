//https://google.github.io/comprehensive-rust/concurrency/sync-exercises/dining-philosophers.html
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Duration;

struct Fork;

struct Philosopher {
    name: String,
    left_fork: Arc<Mutex<Fork>>,
    right_fork: Arc<Mutex<Fork>>,
    thoughts: mpsc::SyncSender<String>,
}

impl Philosopher {
    fn think(&self) {
        self.thoughts
            .send(format!("Eureka! {} has a new idea!", &self.name))
            .unwrap();
    }

    fn eat(&self) {
        // Pick up forks...
        println!("{} is trying to eat...", &self.name);
        let _left = self.left_fork.lock().unwrap();
        let _right = self.right_fork.lock().unwrap();
        println!("{} is eating...", &self.name);
        thread::sleep(Duration::from_millis(10));
    }
}

static PHILOSOPHERS: &[&str] = &["Socrates", "Hypatia", "Plato", "Aristotle", "Pythagoras"];

fn main() {
    let (tx, rx) = mpsc::sync_channel(100);

    let forks: Vec<_> = (0..PHILOSOPHERS.len())
        .map(|_| Arc::new(Mutex::new(Fork)))
        .collect();

    let mut count = 0;
    for i in 0..forks.len() {
        let tx = tx.clone();
        let left_fork = Arc::clone(&forks[i]);
        let right_fork = Arc::clone(&forks[(i + 1) % forks.len()]);

        //if i == forks.len() - 1 {
        //    std::mem::swap(&mut left_fork, &mut right_fork);
        //}

        let philo = Philosopher {
            name: PHILOSOPHERS[i].to_string(),
            left_fork,
            right_fork,
            thoughts: tx,
        };
        thread::spawn(move || {
            for _ in 0..100 {
                count += 1;
                philo.eat();
                philo.think();
            }
        });
    }

    drop(tx);
    for thought in rx {
        println!("{thought}");
    }
    println!("->> count; main function; main.rs\n{:?}", count);
}
