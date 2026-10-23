"""Explicit optional live Azure Search exercise. No service is provisioned here."""
import argparse
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SearchableField, SimpleField, SearchFieldDataType
from .core import read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['upload', 'query'])
    args = parser.parse_args()
    names = ['AZURE_SEARCH_ENDPOINT', 'AZURE_SEARCH_INDEX', 'AZURE_SEARCH_ADMIN_KEY' if args.operation == 'upload' else 'AZURE_SEARCH_QUERY_KEY']
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        parser.error('Missing configuration: ' + ', '.join(missing))
    endpoint, index_name, key = (os.environ[name] for name in names)
    credential = AzureKeyCredential(key)
    if args.operation == 'upload':
        with SearchIndexClient(endpoint, credential) as admin:
            if index_name in admin.list_index_names():
                parser.error('Index already exists. Choose a new owned practice index name; no overwrite performed.')
            fields = [SimpleField(name='id', type=SearchFieldDataType.String, key=True), SearchableField(name='content', type=SearchFieldDataType.String)]
            fields += [SimpleField(name=name, type=SearchFieldDataType.String, filterable=True) for name in ['entity_type', 'jurisdiction', 'effective_from', 'effective_to']]
            admin.create_index(SearchIndex(name=index_name, fields=fields))
        with SearchClient(endpoint, index_name, credential) as client:
            results = client.upload_documents(read_json('policies.json'))
            failures = [r.key for r in results if not r.succeeded]
            if failures:
                raise RuntimeError(f'Upload failed for practice policy IDs: {failures}')
            print(f'Uploaded {len(results)} fictional policies; indexing may take a short time.')
    else:
        # Fixed exercise values avoid introducing unescaped user text into OData.
        scope = "entity_type eq 'COMPANY' and jurisdiction eq 'XA' and effective_from le '2026-11-05' and effective_to gt '2026-11-05'"
        with SearchClient(endpoint, index_name, credential) as client:
            print([hit['id'] for hit in client.search(search_text='review', filter=scope, select=['id'])])


if __name__ == '__main__':
    main()
