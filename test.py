data = {
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.0023064255,
        -0.009327292,
        -0.0028842222,
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}


print(data['data'][0]['embedding'])

for i in range(len(content)):
            # create embedding
            response = self.client.embeddings.create(model='text-embedding-large', input=content[i]['content'], encoding_format='float')
            content[i]['embedding'] = response['embedding']