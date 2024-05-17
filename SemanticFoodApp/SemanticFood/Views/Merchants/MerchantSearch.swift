import SwiftUI

struct MerchantSearch: View {
    @State private var searchText = ""
    @State private var model = MerchantsViewModel()
    @State private var merchants = [Merchant]()
    
    
    var body: some View {
        NavigationStack {
            MerchantList(title: "", merchants: merchants)
        }
        .searchable(text: $searchText, prompt: "Buscar em todo o SematicFood")
        .onSubmit(of: .search, runSearch)
        .onAppear{
            runSearch()
        }
    }
    
    func runSearch() {
        Task {
            merchants = try await model.search(name: searchText)
        }
    }
}

#Preview {
    MerchantSearch()
}
