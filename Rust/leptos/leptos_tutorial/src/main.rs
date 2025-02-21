use std::collections::HashMap;

//
//Eventos: https://docs.rs/leptos/latest/leptos/tachys/html/event/index.html
//Em maiúsculo, são os event handlers iguais a "on:"
//Em minúsculo, são os eventos a serem utilizados, como "click"
//
use leptos::{ev::SubmitEvent, prelude::*};
use leptos_router::{components::*, path};
use reactive_stores::{Patch, Store, StoreFieldIterator};
fn main() {
    console_error_panic_hook::set_once();
    leptos::mount::mount_to_body(App);
}

#[component]
fn App() -> impl IntoView {
    let (count, set_count) = signal(0);
    let message_about_parity = move || {
        if (move || count.get() % 2 == 0)() {
            Some("Eveeenn")
        } else {
            None
        }
    };
    let (count2, set_count2) = signal(1);
    let triple_count = move || count2.get() * 3;
    let list = vec![0, 1, 2];
    let length = 5;
    //using RwSignal is just more practical to not have to use a counter and set_counter
    let counters = (1..=length).map(|idx| RwSignal::new(idx));
    let counter_buttons = counters
        .map(|x| {
            view! {
                <li>
                    <button on:click=move |_| *x.write() += 1></button>
                    {x}

                </li>
            }
        })
        .collect::<Vec<_>>();
    let (parent_toggle, parent_set_toggle) = signal(false);
    provide_context(parent_set_toggle);

    view! {
        <Router>
            <main>
                <button
                    on:click=move |_| {
                        *set_count.write() += 1;
                    }
                    // the class: syntax reactively updates a single class
                    // here, we'll set the `red` class when `count` is odd
                    class=("red", move || count.get() % 2 == 1)
                >
                    "Click me to change class. Number: "
                    {move || count.get()}
                </button>
                <h2>"Basic rust operations with the first counter"</h2>
                // Although possible to write inside of view, better to be outside for cargo fmt and
                // rust-analyzer
                <p>{move || if (move || count.get() % 2 == 0)() { "Even" } else { "Odd" }}</p>
                <h2>"Another basic, but with options"</h2>
                <p>{message_about_parity}</p>
                <button
                    on:click=move |_| {
                        *set_count2.write() += 1;
                    }
                    style="position: relative"
                    style:left=move || format!("{}px", count2.get() * 10)
                    style=(
                        "background-color",
                        move || format!("rgb({}, {}, 100)", count2.get() * 10, 100),
                    )
                    style:max-width="400px"
                    style=("--columns", move || count2.get().to_string())
                >
                    "Click me to change style and move right. Number: "
                    {move || count2.get()}
                </button>
                <br />
                <ProgressBar progress=move || count2.get() />
                <br />
                <ProgressBar max=20 progress=move || count2.get() />
                <br />
                <ProgressBar max=30 progress=triple_count />
                <p>"Triple count2: " {triple_count}</p>
                // Static views
                <h2>"Simple static views"</h2>
                <p>{list.clone()}</p>
                <ul>
                    {list.clone().into_iter().map(|n| view! { <li>{n}</li> }).collect::<Vec<_>>()}
                </ul>
                <ul>{list.into_iter().map(|n| view! { <li>{n}</li> }).collect_view()}</ul>
                // Meio ruim counter_buttons. Quando qualquer um muda, todos sao recalculados
                <h2>
                    "Static List: use this, if the list itself is static, the other parts (such as its elements) don't need to be"
                </h2>
                <ul>{counter_buttons}</ul>
                // Solucao em 3.4. Iteration do book
                <h2>"Dynamic List: renders just the element that changes"</h2>
                <DynamicList initial_length=5 />
                <h2>"Dynamic List 2: More complex case with signal"</h2>
                <DynamicListComplex1/>
                <h2>"Dynamic List 3: More complex case with stores"</h2>
                <DynamicListComplex2/>
                <h2>"Form controlled by framework"</h2>
                <FormControlled />
                <h2>"Form controlled by browser"</h2>
                <FormUncontrolled />
                <h2>"Text Area"</h2>
                <TextArea />
                <h2>"Select"</h2>
                <Select />
                <h2>"Rerender an if only when the statement change and not the value"</h2>
                <ShowComponent count=count />
                <h2>"How to handle error cases"</h2>
                <ErrorExample />
                <h2>"Parent/Child communication"</h2>
                <p>"Toggled? "{parent_toggle}</p>
                <ButtonA setter=parent_set_toggle />
                <ButtonB on_click=move |_| parent_set_toggle.update(|value| *value = !*value) />
                //This is the recomended approach, but be very careful to not mess states
                //It's even faster and less boilerplate, since you don't have to pass the paremeter all the
                //way down
                <ButtonCIntermediate />
                <output>"Ola"</output>
                <Routes fallback=|| "Not found.">
                    <ParentRoute path=path!("/contacts") view=ContactList>
                        <ParentRoute path=path!(":id") view=ContactInfo>
                            <Route path=path!("") view=Email />
                            <Route path=path!("address") view=Address />
                            <Route path=path!("messages") view=Messages />
                        </ParentRoute>
                        <Route
                            path=path!("")
                            view=|| view! { <p>"Select a contact to view more info."</p> }
                        />
                    </ParentRoute>
                    <Route path=path!("/*any") view=|| view! { <h1>"Not Found"</h1> } />
                </Routes>
                <DropdownCheckBox/>
            </main>
        </Router>
    } //view!
}

#[component]
fn ProgressBar(
    #[prop(default = 100)] max: u16,
    progress: impl Fn() -> i32 + Send + Sync + 'static,
) -> impl IntoView {
    view! {
        <progress
            max=max
            // signals are functions, so `value=count` and `value=move || count.get()`
            // are interchangeable.
            value=progress
        />
    }
}

#[component]
fn DynamicList(initial_length: usize) -> impl IntoView {
    let mut next_counter_id = initial_length;

    let initial_counters = (0..initial_length)
        .map(|id| (id, ArcRwSignal::new(id + 1)))
        .collect::<Vec<_>>();
    //Instead of passing this list directly, as in the static case, put this list inside a signal
    let (counters, set_counters) = signal(initial_counters);

    let add_counter = move |_| {
        //using ArcRwSignal allows each signal to be deallocated when its row is removed.
        let sig = ArcRwSignal::new(next_counter_id + 1);
        set_counters.update(move |counters| {
            //".update" gives "&mut T", so we can use Vec methods normally
            counters.push((next_counter_id, sig))
        });
        next_counter_id += 1;
    };
    view! {
        <div>
            <button on:click=add_counter>"Add Counter"</button>
            <ul>
                <For
                    // `each` takes any function that returns an iterator
                    // if it's not reactive, just render a Vec<_> instead of <For/>
                    each=move || counters.get()
                    // the key should be unique and stable for each row
                    // using an index is usually a bad idea, unless your list
                    // can only grow, because moving items around inside the list
                    // means their indices will change and they will all rerender
                    key=|counter| counter.0
                    children=move |(id, count)| {
                        let count = RwSignal::from(count);
                        // we can convert our ArcRwSignal to a Copy-able RwSignal
                        // for nicer DX when moving it into the view
                        view! {
                            <li>
                                <button on:click=move |_| *count.write() += 1>{count}</button>
                                <button on:click=move |_| {
                                    set_counters
                                        .write()
                                        .retain(|(counter_id, _)| { counter_id != &id });
                                }>"Remove"</button>
                            </li>
                        }
                    }
                />
            </ul>
        </div>
    }
}

//Continuar daqui para loops mais complicados
//https://book.leptos.dev/view/04b_iteration.html
#[derive(Debug, Clone)]
struct DatabaseEntry {
    key: String,
    value: RwSignal<i32>,
}

#[component]
fn DynamicListComplex1() -> impl IntoView {
    // start with a set of three rows
    let (data, set_data) = signal(vec![
        DatabaseEntry {
            key: "foo".to_string(),
            value: RwSignal::new(10),
        },
        DatabaseEntry {
            key: "bar".to_string(),
            value: RwSignal::new(20),
        },
        DatabaseEntry {
            key: "baz".to_string(),
            value: RwSignal::new(15),
        },
    ]);
    view! {
        // when we click, update each row,
        // doubling its value
        <button on:click=move |_| {
            for row in &*data.read() {
                row.value.update(|value| *value *= 2);
            }
            // log the new value of the signal
            leptos::logging::log!("{:?}", data.get());
        }>
            "Update Values"
        </button>
        // iterate over the rows and display each value
        <For
            each=move || data.get()
            key=|state| state.key.clone()
            let:child
        >
            <p>{child.value}</p>
        </For>
    }
}

#[derive(Store, Debug, Clone)]
pub struct Data {
    #[store(key: String = |row| row.key.clone())]
    rows: Vec<DatabaseEntry2>,
}

#[derive(Store, Debug, Clone)]
struct DatabaseEntry2 {
    key: String,
    value: i32,
}

#[component]
pub fn DynamicListComplex2() -> impl IntoView {
    // instead of a single with the rows, we create a store for Data
    let data = Store::new(Data {
        rows: vec![
            DatabaseEntry2 {
                key: "foo".to_string(),
                value: 10,
            },
            DatabaseEntry2 {
                key: "bar".to_string(),
                value: 20,
            },
            DatabaseEntry2 {
                key: "baz".to_string(),
                value: 15,
            },
        ],
    });

    view! {
        // when we click, update each row,
        // doubling its value
        <button on:click=move |_| {
            // calling rows() gives us access to the rows
            // .iter_unkeyed
            for row in data.rows().iter_unkeyed() {
                *row.value().write() *= 2;
            }
            // log the new value of the signal
            leptos::logging::log!("{:?}", data.get());
        }>
            "Update Values"
        </button>
        // iterate over the rows and display each value
        <For
            each=move || data.rows()
            key=|row| row.read().key.clone()
            children=|child| {
                let value = child.value();
                view! { <p>{move || value.get()}</p> }
            }
        />
    }
}

//Framework controls the state of the input
fn FormControlled() -> impl IntoView {
    let (name, set_name) = signal("Controlled".to_string());
    view! {
        <input
            type="text"
            on:input:target=move |ev| {
                set_name.set(ev.target().value());
            }
            prop:value=name
        />
        <p>"Name is: "{name}</p>
    }
}

//Browser controls the state of the input
fn FormUncontrolled() -> impl IntoView {
    let (name, set_name) = signal("Uncontrolled".to_string());

    let input_element: NodeRef<leptos::html::Input> = NodeRef::new();

    let on_submit = move |ev: SubmitEvent| {
        ev.prevent_default();
        let value = input_element
            .get()
            .expect("<input> should be mounted")
            .value();
        set_name.set(value);
    };

    view! {
        <form on:submit=on_submit>
            <input type="text" value=name node_ref=input_element />
            <input type="submit" value="Submit" />
        </form>
        <p>"Name is: " {name}</p>
    }
}

fn TextArea() -> impl IntoView {
    let value = RwSignal::new("".to_string());
    view! {
        <textarea
            prop:value=move || value.get()
            on:input:target=move |ev| value.set(ev.target().value())
        >

            {value.get_untracked()}
        </textarea>
    }
}

fn Select() -> impl IntoView {
    let (value, set_value) = signal(0i32);
    view! {
        <select
            on:change:target=move |ev| {
                set_value.set(ev.target().value().parse().unwrap());
            }
            prop:value=move || value.get().to_string()
        >
            <option value="0">"0"</option>
            <option value="1">"1"</option>
            <option value="2">"2"</option>
        </select>
        // a button that will cycle through the options
        <button on:click=move |_| {
            set_value
                .update(|n| {
                    if *n == 2 {
                        *n = 0;
                    } else {
                        *n += 1;
                    }
                })
        }>"Next Option"</button>
    }
}

#[component]
fn ShowComponent(count: ReadSignal<usize>) -> impl IntoView {
    //Could have been match
    //If branchs do not have the same view, it won't compile. Solution is to use an enum
    view! {
        <Show
            when=move || { count.get() > 5 }
            fallback=|| view! { <p>"Smaller than or equal to 5"</p> }
        >
            <p>"Bigger than 5"</p>
        </Show>
    }
}

#[component]
fn ErrorExample() -> impl IntoView {
    let (value, set_value) = signal(Ok(0));

    view! {
        <label>
            "Type an integer:"
            <input
                type="number"
                on:input:target=move |ev| { set_value.set(ev.target().value().parse::<i32>()) }
            /> // In case of Err, returns this
            <ErrorBoundary fallback=|errors| {
                view! {
                    <div class="error">
                        <p>"Not an integer. Errors: "</p>
                        <ul>
                            {move || {
                                errors
                                    .get()
                                    .into_iter()
                                    .map(|(_, e)| view! { <li>{e.to_string()}</li> })
                                    .collect::<Vec<_>>()
                            }}
                        </ul>
                    </div>
                }
            }>
                <p>"You entered " <strong>{value}</strong></p>
            </ErrorBoundary>
        </label>
    }
}

#[component]
fn ButtonA(setter: WriteSignal<bool>) -> impl IntoView {
    view! { <button on:click=move |_| setter.update(|value| *value = !*value)>"Toggle"</button> }
}

#[component]
fn ButtonB(on_click: impl FnMut(leptos::ev::MouseEvent) + 'static) -> impl IntoView {
    view! { <button on:click=on_click>"Toggle"</button> }
}

#[component]
fn ButtonCIntermediate() -> impl IntoView {
    view! {
        <div class="content">
            <ButtonC />
        </div>
    }
}

#[component]
fn ButtonC() -> impl IntoView {
    let setter = use_context::<WriteSignal<bool>>().expect("to have found the setter");
    view! { <button on:click=move |_| setter.update(|value| *value = !*value)>"Toggle"</button> }
}

#[component]
fn Home() -> impl IntoView {
    view! { <p><br/>"Home"</p> }
}

#[component]
fn Users() -> impl IntoView {
    view! { <p><br/>"Users"</p> }
}

#[component]
fn UserProfile() -> impl IntoView {
    view! { <p><br/>"UserProfile"</p> }
}

#[component]
fn ContactList() -> impl IntoView {
    view! { <p><br/>"ContactList"</p>
        <div style="display: flex">
            <ContactInfo/>
            <Outlet/>
            </div>
    }
}
#[component]
fn ContactInfo() -> impl IntoView {
    view! { <p><br/>"ContactInfo"</p> }
}
#[component]
fn Email() -> impl IntoView {
    view! { <p><br/>"Email"</p> }
}
#[component]
fn Address() -> impl IntoView {
    view! { <p><br/>"Address"</p> }
}
#[component]
fn Messages() -> impl IntoView {
    view! { <p><br/>"Messages"</p> }
}

#[component]
fn DropdownCheckBox() -> impl IntoView {
    let companies_vec = vec!["appl", "googl", "tsm"];
    let boxed_dictionary: HashMap<&str, RwSignal<bool>> = companies_vec
        .iter()
        .map(|name| (*name, RwSignal::new(false)))
        .collect();
    let companies = companies_vec.into_iter().map(|name| RwSignal::new(name));
    let company_checkbox = companies
        .map(|name| {
            view! {
                <div>
                    <input type="checkbox" bind:checked=*boxed_dictionary.get(name.get()).expect(">>> Couldn't get dictionary key")></input>
                    {name}

                </div>
            }
        })
        .collect::<Vec<_>>();
    println!("{:?}", boxed_dictionary);
    view! {
        <ul>{company_checkbox}</ul>
        <p>{boxed_dictionary.get("appl").unwrap()}</p>
    }
}
