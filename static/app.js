const e = React.createElement;

function App() {
    const [query, setQuery] = React.useState("");
    const [results, setResults] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState("");

    const [page, setPage] = React.useState(1);
    const [total, setTotal] = React.useState(0);

    const [minPrice, setMinPrice] = React.useState("");
    const [maxPrice, setMaxPrice] = React.useState("");

    function search(p = 1) {
        if (!query.trim()) return;

        setLoading(true);
        setError("");
        setResults([]);
        setPage(p);

        const params = new URLSearchParams({
            q: query,
            page: p,
            min_price: minPrice,
            max_price: maxPrice
        });

        fetch(`/search?${params}`)
            .then(res => res.json())
            .then(data => {
                setResults(data.results || []);
                setTotal(data.total || 0);
            })
            .catch(() => setError("Erro de ligação com o servidor."))
            .finally(() => setLoading(false));
    }

    const totalPages = Math.ceil(total / 9);

    return e("div", { className: "container my-5" }, [

        /* HEADER */
        e("div", { className: "text-center mb-5" }, [
            e("h1", { style: { fontWeight: 700 } }, "Find In"),
            e("p", { className: "text-muted" }, "Encontre os melhores produtos no melhor preço")
        ]),

        /* SEARCH */
        e("div", { className: "card shadow-lg border-0 p-4 mb-5", style: { borderRadius: "16px" } }, [
            e("div", { className: "row g-3" }, [
                e("div", { className: "col-md-6" },
                    e("input", {
                        className: "form-control form-control-lg",
                        placeholder: "Pesquisar produto",
                        value: query,
                        onChange: ev => setQuery(ev.target.value),
                        onKeyDown: ev => ev.key === "Enter" && search(1)
                    })
                ),
                e("div", { className: "col-md-3" },
                    e("input", {
                        className: "form-control form-control-lg",
                        placeholder: "Preço mín (€)",
                        value: minPrice,
                        onChange: ev => setMinPrice(ev.target.value)
                    })
                ),
                e("div", { className: "col-md-3" },
                    e("input", {
                        className: "form-control form-control-lg",
                        placeholder: "Preço máx (€)",
                        value: maxPrice,
                        onChange: ev => setMaxPrice(ev.target.value)
                    })
                )
            ]),
            e("div", { className: "d-grid mt-4" },
                e("button", {
                    className: "btn btn-primary btn-lg",
                    onClick: () => search(1)
                }, loading ? "A pesquisar..." : "Pesquisar")
            )
        ]),

        /* LOADING */
        loading && e("div", { className: "text-center my-5" },
            e("div", { className: "spinner-border text-primary" })
        ),

        /* ERROR */
        error && e("div", { className: "alert alert-danger text-center" }, error),

        /* RESULTS */
        e("div", { className: "row g-4" },
            results.map((item, idx) =>
                e("div", { className: "col-md-4", key: idx },
                    e("div", {
                        className: "card h-100 border-0 shadow-sm",
                        style: { borderRadius: "16px", overflow: "hidden" }
                    }, [

                        /* IMAGE */
                        e("div", {
                            style: {
                                height: "200px",
                                background: `url(${item.image || "https://via.placeholder.com/400"}) center / contain no-repeat`,
                                backgroundColor: "#bbbbbbff"
                            }
                        }),

                        e("div", { className: "card-body d-flex flex-column" }, [
                            e("h6", { style: { fontWeight: 600 } }, item.title),

                            /* PRICES */
                            e("div", { className: "mt-2" }, [
                                e("div", { className: "fw-bold text-primary fs-5" },
                                    item.price ? `Preço: € ${item.price}` : "Preço N/D"
                                ),
                                item.price_kz && e("div", {
                                    className: "text-muted small"
                                }, `≈ Kz ${item.price_kz}`)
                            ]),

                            /* STORE + LOCATION */
                            e("p", { className: "text-muted small mt-2 mb-3" },
                                `Loja: ${item.store || "Loja desconhecida"}${item.location ? " • " + item.location : ""}`
                            ),

                            /*e("a", {
                                href: item.link,
                                target: "_blank",
                                className: "btn btn-outline-primary mt-auto"
                            }, "Ver produto")*/
                        ])
                    ])
                )
            )
        ),

        /* EMPTY */
        (!loading && query && results.length === 0) &&
        e("p", { className: "text-center text-muted mt-5" },
            "Nenhum resultado encontrado."
        ),

        /* PAGINATION */
        totalPages > 1 &&
        e("nav", { className: "mt-5" },
            e("ul", { className: "pagination justify-content-center" },
                Array.from({ length: totalPages }, (_, i) =>
                    e("li", {
                        className: `page-item ${page === i + 1 ? "active" : ""}`,
                        key: i
                    },
                        e("button", {
                            className: "page-link",
                            onClick: () => search(i + 1)
                        }, i + 1)
                    )
                )
            )
        )
    ]);
}

ReactDOM.createRoot(document.getElementById("root")).render(e(App));